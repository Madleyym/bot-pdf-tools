from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
from fpdf import FPDF
import os
import time
import json
from datetime import datetime


def create_progress_log(pdf_path, total_pages):
    """Create or load progress log file"""
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    log_file = f"progress_{base_name}.json"

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            return json.load(f)

    return {
        "filename": base_name,
        "total_pages": total_pages,
        "processed_pages": [],
        "failed_pages": [],
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_processed_page": 0,
    }


def save_progress(progress_data):
    """Save progress to log file"""
    log_file = f"progress_{progress_data['filename']}.json"
    with open(log_file, "w") as f:
        json.dump(progress_data, f, indent=4)


def translate_text(text, target_lang="id"):
    try:
        chunk_size = 4500
        chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

        translated_chunks = []
        translator = GoogleTranslator(source="auto", target=target_lang)

        for chunk in chunks:
            translated_chunk = translator.translate(chunk)
            if translated_chunk:
                translated_chunks.append(translated_chunk)
            time.sleep(1)

        return " ".join(translated_chunks)
    except Exception as e:
        print(f"Error in translation: {str(e)}")
        return None


def save_partial_translation(translated_text, page_num, base_name):
    """Save translated text for each page"""
    partial_dir = "partial_translations"
    if not os.path.exists(partial_dir):
        os.makedirs(partial_dir)

    partial_file = os.path.join(partial_dir, f"{base_name}_page_{page_num}.txt")
    with open(partial_file, "w", encoding="utf-8") as f:
        f.write(translated_text)


def process_pdf(pdf_path):
    try:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        # Initialize or load progress
        progress = create_progress_log(pdf_path, total_pages)
        print(f"\nProcessing: {pdf_path}")
        print(f"Total pages: {total_pages}")

        # Create directory for partial translations if it doesn't exist
        partial_dir = "partial_translations"
        if not os.path.exists(partial_dir):
            os.makedirs(partial_dir)

        # Start from last processed page
        start_page = progress["last_processed_page"]

        for i in range(start_page, total_pages):
            try:
                print(f"\nProcessing page {i+1} of {total_pages}...")
                print(f"Progress: {((i+1)/total_pages)*100:.2f}%")

                # Check if page was already processed
                if i in progress["processed_pages"]:
                    print(f"Page {i+1} already processed, skipping...")
                    continue

                text = reader.pages[i].extract_text()
                if text:
                    text = "".join(char for char in text if ord(char) < 65536)
                    translated_text = translate_text(text)

                    if translated_text:
                        # Save each translated page separately
                        save_partial_translation(translated_text, i + 1, base_name)
                        progress["processed_pages"].append(i)
                        print(f"✓ Page {i+1} translated and saved")
                    else:
                        progress["failed_pages"].append(i)
                        print(f"✗ Failed to translate page {i+1}")

                progress["last_processed_page"] = i
                save_progress(progress)

                # Show current statistics
                success_rate = (len(progress["processed_pages"]) / total_pages) * 100
                print(f"\nCurrent Statistics:")
                print(
                    f"Successfully translated: {len(progress['processed_pages'])} pages ({success_rate:.2f}%)"
                )
                print(f"Failed pages: {len(progress['failed_pages'])}")

            except Exception as e:
                print(f"Error on page {i+1}: {str(e)}")
                progress["failed_pages"].append(i)
                save_progress(progress)
                continue

        # After all pages are processed, combine into final PDF
        if len(progress["processed_pages"]) > 0:
            try:
                print("\nCreating final PDF...")
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)

                for i in range(total_pages):
                    partial_file = os.path.join(
                        partial_dir, f"{base_name}_page_{i+1}.txt"
                    )
                    if os.path.exists(partial_file):
                        with open(partial_file, "r", encoding="utf-8") as f:
                            content = f.read()
                            pdf.add_page()
                            pdf.set_font("Arial", size=12)
                            pdf.multi_cell(0, 10, content)

                output_file = f"translated_{base_name}.pdf"
                pdf.output(output_file)
                print(f"\nFinal PDF created: {output_file}")

                # Add completion time to progress log
                progress["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_progress(progress)

            except Exception as e:
                print(f"Error creating final PDF: {str(e)}")
                return False

        return True
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return False


def main():
    pdf_folder = (
        r"C:\Users\twenty-one\Desktop\Xian Ni - Renegade Immortal\bot-pdf-tools\PDF"
    )

    print("=== PDF Translator with Real-time Progress ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Looking for PDFs in: {pdf_folder}")

    if not os.path.exists(pdf_folder):
        print(f"Error: The folder '{pdf_folder}' does not exist!")
        return

    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the specified folder!")
        return

    print(f"Found {len(pdf_files)} PDF files to process.")
    print("\nProcessing order:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"{i}. {pdf_file}")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"\n{'='*50}")
        print(f"Starting file: {pdf_file}")
        process_pdf(pdf_path)

    print(f"\n{'='*50}")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
