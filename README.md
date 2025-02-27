# IMG-2-TEXT

A powerful Streamlit application for extracting text from images using Tesseract OCR engine. This tool provides a user-friendly interface to convert visual text into editable, searchable content.

## Features

- **Multi-format Support**: Extract text from JPG, PNG and JPEG image formats
- **Batch Processing**: Upload and process multiple files simultaneously
- **Enhanced Text Extraction**: Grayscale conversion for improved OCR accuracy
- **Instant Results**: View extracted text directly in the application
- **Export Functionality**: Download extracted text as .txt files
- **Responsive UI**: Clean, intuitive interface built with Streamlit

## Requirements

- Python 3.10 or higher
- Tesseract OCR engine installed on your system
- Dependencies listed in `pyproject.toml`

## Installation

This project uses Poetry for dependency management, ensuring consistent installations across environments.

### 1. Install Python 3.10+

Make sure you have Python 3.10 or higher installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### 2. Install Poetry

If you don't have Poetry installed, you can install it using:

```bash
# For Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# For macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Clone and Setup

```bash
# Clone the repository (if using git)
git clone https://github.com/kkhatke/IMG-2-TEXT.git
cd image-ocr-tool

# Or simply create a new directory and add the files
mkdir image-ocr-tool
cd image-ocr-tool
# [Add pyproject.toml and app.py files here]

# Install dependencies
poetry install
```

## Tesseract OCR Installation

### Windows
1. Download the installer from [UB-Mannheim's GitHub repository](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer and follow the instructions
3. Default installation path is `C:\Program Files\Tesseract-OCR\`
4. Ensure the path in `app.py` matches your installation path

### macOS
```bash
brew install tesseract
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr
```

## Usage

1. Start the application:
   ```bash
   poetry run streamlit run app.py
   ```

2. Your browser will automatically open to the application (typically at http://localhost:8501)

3. Upload your images using the file uploader

4. The application will process each file and display the extracted text

5. Expand the text sections to view complete extracted content

6. Download any extracted text as a .txt file using the provided download buttons

## How It Works

1. The application accepts image files through the Streamlit interface
2. Images are processed directly
3. Each image is converted to grayscale to improve OCR accuracy
4. Tesseract OCR processes the images to extract text content
5. Results are displayed in the UI and made available for download

## Project Structure

```
image-ocr-tool/
├── app.py                 # Main Streamlit application
├── pyproject.toml         # Poetry configuration and dependencies
└── README.md              # This documentation file
```

## Future Improvements

- Add language selection for multilingual OCR
- Implement image preprocessing options (contrast adjustment, noise reduction)
- Create custom output formatting options
- Add OCR accuracy metrics
- Support for table extraction and structured data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


