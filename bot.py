from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
from fpdf import FPDF
import os

def translate_text(text, target_lang="id"):
    try:
        translator = GoogleTranslator(source="auto", target=target_lang)
        return translator.translate(text)
    except Exception as e:
        print(f"Error in translation: {str(e)}")
        return text

def process_pdf(pdf_path):
    try:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_file = f"translated_{base_name}.pdf"

        print(f"\nProcessing: {pdf_path}")
        reader = PdfReader(pdf_path)
        translated_text = []

        total_pages = len(reader.pages)
        for i, page in enumerate(reader.pages, 1):
            print(f"Translating page {i} of {total_pages}...")
            text = page.extract_text()
            if text:
                translated_text.append(translate_text(text))

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        for translated_page in translated_text:
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, translated_page)

        output_path = os.path.join(os.path.dirname(pdf_path), output_file)
        pdf.output(output_path)
        print(f"Translation completed! Saved as: {output_path}")

        return True
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return False


def main():
    pdf_folder = (
        r"C:\Users\twenty-one\Desktop\Xian Ni - Renegade Immortal\bot-pdf-tools\PDF"
    )

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

    successful = 0
    failed = 0

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"\n{'='*50}")
        print(f"Processing file {pdf_file}...")

        if process_pdf(pdf_path):
            successful += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print("Processing Complete!")
    print(f"Successfully processed: {successful} files")
    print(f"Failed to process: {failed} files")

if __name__ == "__main__":
    main()
