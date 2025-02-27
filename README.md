# PDF Translation Bot

A Python-based tool that automatically translates PDF documents from English to Indonesian using Google Translate API.

## Features

- 🔄 English to Indonesian translation
- 📚 Batch processing of multiple PDF files
- 📁 Organized output with prefix "translated_"
- 📊 Progress tracking during translation
- ⚡ Fast processing
- 🛠️ Robust error handling

## Prerequisites

Before running this tool, make sure you have:
- Python 3.x installed
- Internet connection (required for translation)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Madleyym/bot-pdf-tools.git
cd bot-pdf-tools
```

2. Install the required dependencies:
```bash
pip install PyPDF2 deep-translator fpdf
```

## Directory Structure

```
bot-pdf-tools/
│
├── PDF/                    # Place your English PDF files here
├── bot.py                 # Main script
└── README.md              # This file
```

## Usage

1. Place your English PDF files in the `PDF` folder.

2. Run the script:
```bash
python bot.py
```

3. The script will:
   - Process all English PDF files in the PDF folder
   - Translate the content to Indonesian
   - Create translated versions with prefix "translated_"
   - Show progress for each file and page
   - Display a summary of successful and failed translations

## Configuration

The script is configured to:
- Read English PDFs from: `C:\Users\twenty-one\Desktop\Xian Ni - Renegade Immortal\bot-pdf-tools\PDF`
- Translate from English to Indonesian
- Save translated files in the same folder with "translated_" prefix

## Error Handling

The script includes comprehensive error handling for:
- Missing PDF files or folders
- Translation errors
- File access issues
- PDF reading/writing errors

## Output Examples

Input file: `chapter1.pdf` (English)
Output file: `translated_chapter1.pdf` (Indonesian)

## Contributing

Feel free to:
- Report issues
- Submit pull requests
- Suggest improvements
- Share your feedback

## Author

- **Madleyym**
- Created: 2025-02-27 01:42:31 UTC

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyPDF2 for PDF processing
- deep-translator for translation services
- FPDF for PDF creation

## Important Notes

1. This tool is specifically designed for English to Indonesian translation
2. Make sure your PDF files contain readable English text
3. The quality of translation depends on Google Translate's accuracy
4. Large PDF files may take longer to process