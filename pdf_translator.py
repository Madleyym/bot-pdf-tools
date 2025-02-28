from deep_translator import GoogleTranslator
import fitz  # PyMuPDF
import os
import time
from datetime import datetime
import re
from fpdf import FPDF


class PDFTranslator:
    def __init__(self):
        # Create folders if they don't exist
        self.pdf_folder = "PDF"
        self.output_folder = "hasil_terjemahan"

        for folder in [self.pdf_folder, self.output_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder: {folder}")

    def get_pdf_list(self):
        """Get list of PDF files and let user select one"""
        pdf_files = [
            f for f in os.listdir(self.pdf_folder) if f.lower().endswith(".pdf")
        ]

        if not pdf_files:
            print("Tidak ada file PDF di folder PDF!")
            return []

        print("\nDaftar PDF yang tersedia:")
        for i, pdf in enumerate(pdf_files, 1):
            print(f"{i}. {pdf}")

        while True:
            try:
                choice = int(
                    input(
                        "\nPilih nomor PDF yang ingin diterjemahkan (0 untuk keluar): "
                    )
                )
                if choice == 0:
                    return []
                if 1 <= choice <= len(pdf_files):
                    return [pdf_files[choice - 1]]
                print("Nomor tidak valid!")
            except ValueError:
                print("Masukkan nomor yang valid!")

    def is_image_page(self, page):
        """Check if page has minimal text and likely contains mostly images"""
        text = page.get_text().strip()
        # If page has less than 100 characters and has images
        if len(text) < 100 and len(page.get_images()) > 0:
            return True
        return False

    def translate_text(self, text, target="id"):
        """Translate text from English to target language"""
        if not text or len(text.strip()) < 5:  # Skip very short texts
            return text

        # Clean the text - remove excessive whitespace
        text = re.sub(r"\s+", " ", text).strip()

        try:
            translator = GoogleTranslator(source="auto", target=target)
            return translator.translate(text)
        except Exception as e:
            print(f"Error translating: {str(e)}")
            # Try again after delay
            try:
                time.sleep(2)
                return translator.translate(text)
            except:
                return text  # Return original on error

    def process_pdf_with_layout_preserved(self, pdf_path):
        """Process PDF and create translated version while preserving layout"""
        print(f"\nMemproses: {pdf_path}")
        
        # Create output directory
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(self.output_folder, f"{base_name}_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        
        # Output file paths
        output_pdf = os.path.join(output_dir, f"terjemahan_{base_name}.pdf")
        output_txt = os.path.join(output_dir, f"terjemahan_{base_name}.txt")
        
        # Open the PDF
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"Total halaman: {total_pages}")
        
        # Create a copy for annotations
        output_doc = fitz.open()
        
        # Text file for translations
        with open(output_txt, "w", encoding="utf-8") as f:
            # Write header
            f.write(f"=== TERJEMAHAN {base_name} ===\n")
            f.write(f"Diterjemahkan pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Process each page
            translated_pages = []
            skipped_pages = []
            
            for page_num in range(total_pages):
                try:
                    page = doc[page_num]
                    print(f"\nMemproses halaman {page_num+1} dari {total_pages}...")
                    
                    # Create new page with same dimensions
                    new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
                    
                    # First copy the original page as background to preserve layout and images
                    new_page.show_pdf_page(new_page.rect, doc, page_num)
                    
                    # Check if it's an image page
                    if self.is_image_page(page):
                        print(f"Halaman {page_num+1} terdeteksi sebagai gambar, mempertahankan asli.")
                        skipped_pages.append(page_num + 1)
                        continue
                    
                    # Extract text blocks for translation
                    blocks = page.get_text("blocks")
                    
                    # Write to text file
                    f.write(f"\n\n--- HALAMAN {page_num+1} ---\n\n")
                    
                    # Add semi-transparent white layer to make original text less visible
                    # (optional - uncomment if you want to make original text fade out)
                    # rect = page.rect
                    # new_page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1, 0.7))
                    
                    # Translate and add text blocks over original
                    for block in blocks:
                        if block[6] == 0:  # text block
                            text = block[4].strip()
                            if len(text) > 5:  # Skip very short blocks
                                rect = fitz.Rect(block[:4])
                                
                                # Translate the text
                                translated = self.translate_text(text)
                                f.write(f"{translated}\n\n")
                                
                                # Add translated text as annotation
                                annot = new_page.add_freetext_annot(
                                    rect,
                                    translated,
                                    fontsize=10,
                                    fontname="helv",
                                    text_color=(0, 0, 0),
                                    fill_color=(1, 1, 1, 0.9),  # Almost opaque white
                                    border_color=(0, 0, 0)
                                )
                                annot.update()
                    
                    translated_pages.append(page_num + 1)
                    print(f"✓ Halaman {page_num+1} berhasil diterjemahkan")
                    
                    # Add delay to avoid API limitations
                    time.sleep(1.5)
                    
                except Exception as e:
                    print(f"Error pada halaman {page_num+1}: {str(e)}")
                    skipped_pages.append(page_num + 1)
            
            # Save the translated PDF
            output_doc.save(output_pdf)
            output_doc.close()
        
        doc.close()
        
        print("\nProses terjemahan selesai:")
        print(f"- Hasil terjemahan (txt): {output_txt}")
        print(f"- Hasil terjemahan (pdf): {output_pdf}")
        print(f"- Halaman diterjemahkan: {len(translated_pages)} dari {total_pages}")
        print(f"- Halaman dilewati: {len(skipped_pages)}")
        
        return True

    def create_pdf_file(self, pdf_path, title, page_contents):
        """Create PDF file from translated content with better encoding handling"""
        # Create PDF
        pdf = FPDF()
        # Important: specify encoding
        pdf.set_margin(15)  # Add margins for better readability
        pdf.set_auto_page_break(True, margin=15)

        # Add title page
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Terjemahan: {title}", 0, 1, "C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.cell(
            0,
            10,
            f"Diterjemahkan pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            0,
            1,
        )
        pdf.ln(10)

        # Add content pages
        for page_data in page_contents:
            pdf.add_page()

            # Page header
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, f"Halaman {page_data['page_num']}", 0, 1)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(5)

            # Page content
            pdf.set_font("Arial", "", 11)

            for paragraph in page_data["content"]:
                # Clean and encode paragraph
                cleaned_text = self.clean_text_for_pdf(paragraph)

                # Write paragraph
                try:
                    pdf.multi_cell(0, 6, cleaned_text)
                    pdf.ln(3)
                except Exception as error:
                    print(f"Skipping problematic text: {str(error)}")

        # Save PDF to file
        pdf.output(pdf_path)

    def create_simple_pdf(self, txt_path, pdf_path, title):
        """Alternative simpler method to create PDF from text file"""
        # Read text file
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Create PDF
        pdf = FPDF()
        pdf.set_auto_page_break(True, margin=15)
        pdf.add_page()

        # Add title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Terjemahan: {title}", 0, 1, "C")
        pdf.ln(5)

        # Split by page markers
        pages = re.split(r"--- HALAMAN \d+ ---", content)

        # Add header
        if len(pages) > 0:
            pdf.set_font("Arial", "", 10)
            header_lines = pages[0].split("\n")
            for line in header_lines:
                if line.strip():
                    pdf.cell(0, 5, line.strip(), 0, 1)
            pdf.ln(5)

        # Add content pages
        for i in range(1, len(pages)):
            pdf.add_page()

            # Page header
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"Halaman {i}", 0, 1)
            pdf.ln(5)

            # Page content
            pdf.set_font("Arial", "", 11)

            # Split into paragraphs
            paragraphs = pages[i].split("\n\n")
            for para in paragraphs:
                if para.strip():
                    # Clean text
                    cleaned = self.clean_text_for_pdf(para)
                    try:
                        pdf.multi_cell(0, 6, cleaned)
                        pdf.ln(3)
                    except:
                        # Skip problematic text
                        pass

        # Save PDF
        pdf.output(pdf_path)

    def clean_text_for_pdf(self, text):
        """Clean text for PDF compatibility"""
        # Replace problematic characters
        replacements = {
            "\u2018": "'",  # Left single quote
            "\u2019": "'",  # Right single quote
            "\u201c": '"',  # Left double quote
            "\u201d": '"',  # Right double quote
            "\u2013": "-",  # En dash
            "\u2014": "--",  # Em dash
            "\u2026": "...",  # Ellipsis
            "\u00a0": " ",  # Non-breaking space
        }

        for char, replacement in replacements.items():
            text = text.replace(char, replacement)

        # Convert to basic ASCII for maximum compatibility
        ascii_text = ""
        for c in text:
            # Keep ASCII characters and common symbols
            if ord(c) < 128:
                ascii_text += c
            else:
                # Replace with closest equivalent or underscore
                ascii_text += "_"

        return ascii_text

    def run(self):
        """Run the translator"""
        print("=== Simple PDF Translator ===")
        print("Program ini menerjemahkan teks PDF dari Bahasa Inggris ke Indonesia")
        print("Output akan tersedia dalam format TXT dan PDF")
        print("Letakkan file PDF di folder 'PDF'")

        while True:
            pdf_files = self.get_pdf_list()
            if not pdf_files:
                break

            for pdf_file in pdf_files:
                pdf_path = os.path.join(self.pdf_folder, pdf_file)
                self.process_pdf_with_layout_preserved(pdf_path)
                
            retry = input("\nIngin menerjemahkan PDF lain? (y/n): ").lower()
            if retry != "y":
                break

        print("\nProgram selesai!")


if __name__ == "__main__":
    translator = PDFTranslator()
    translator.run()
