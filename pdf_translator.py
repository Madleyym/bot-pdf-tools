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

    def process_pdf(self, pdf_path):
        """Process PDF and create translated text and PDF files"""
        print(f"\nMemproses: {pdf_path}")

        # Create output directory
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(self.output_folder, f"{base_name}_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)

        # Output file paths - clearly displayed
        output_txt = os.path.join(output_dir, f"terjemahan_{base_name}.txt")
        output_pdf = os.path.join(output_dir, f"terjemahan_{base_name}.pdf")
        print(f"File yang akan dibuat:\n- TXT: {output_txt}\n- PDF: {output_pdf}")

        # Open the PDF
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"Total halaman: {total_pages}")

        # Collect translated content per page
        translated_pages = []
        skipped_pages = []
        all_pages_content = []

        with open(output_txt, "w", encoding="utf-8") as f:
            # Write header
            f.write(f"=== TERJEMAHAN {base_name} ===\n")
            f.write(
                f"Diterjemahkan pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            # Process each page
            for page_num in range(total_pages):
                try:
                    page = doc[page_num]

                    print(f"\nMemproses halaman {page_num+1} dari {total_pages}...")

                    # Check if it's an image page
                    if self.is_image_page(page):
                        print(
                            f"Halaman {page_num+1} terdeteksi sebagai gambar, dilewati."
                        )
                        skipped_pages.append(page_num + 1)
                        continue

                    # Extract text
                    text = page.get_text()

                    if not text.strip():
                        print(f"Halaman {page_num+1} tidak memiliki teks, dilewati.")
                        skipped_pages.append(page_num + 1)
                        continue

                    # Split text into paragraphs for better translation
                    paragraphs = [
                        p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()
                    ]

                    print(f"Menerjemahkan halaman {page_num+1}...")

                    # Write to text file
                    f.write(f"\n\n--- HALAMAN {page_num+1} ---\n\n")

                    # Store page content for PDF
                    page_content = []

                    # Translate each paragraph
                    for para in paragraphs:
                        if para.strip():
                            translated = self.translate_text(para)
                            f.write(f"{translated}\n\n")
                            page_content.append(translated)

                    all_pages_content.append(
                        {"page_num": page_num + 1, "content": page_content}
                    )

                    translated_pages.append(page_num + 1)
                    print(f"✓ Halaman {page_num+1} berhasil diterjemahkan")

                    # Add delay to avoid API limitations
                    time.sleep(1.5)

                except Exception as e:
                    print(f"Error pada halaman {page_num+1}: {str(e)}")
                    skipped_pages.append(page_num + 1)

        # Create PDF - with extra debugging
        print("\nMembuat file PDF...")
        try:
            self.create_pdf_file(output_pdf, base_name, all_pages_content)
            print(f"✓ PDF berhasil dibuat: {output_pdf}")
        except Exception as e:
            print(f"Error saat membuat PDF: {str(e)}")
            # Try alternative PDF creation
            try:
                print("Mencoba metode alternatif untuk membuat PDF...")
                self.create_simple_pdf(output_txt, output_pdf, base_name)
                print(f"✓ PDF berhasil dibuat dengan metode alternatif: {output_pdf}")
            except Exception as e:
                print(f"Gagal membuat PDF: {str(e)}")

        # Summary
        print("\nProses terjemahan selesai:")
        print(f"- Hasil terjemahan (txt): {output_txt}")
        if os.path.exists(output_pdf):
            print(f"- Hasil terjemahan (pdf): {output_pdf}")
        else:
            print("- PDF tidak berhasil dibuat")
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
                self.process_pdf(pdf_path)

            retry = input("\nIngin menerjemahkan PDF lain? (y/n): ").lower()
            if retry != "y":
                break

        print("\nProgram selesai!")


if __name__ == "__main__":
    translator = PDFTranslator()
    translator.run()
