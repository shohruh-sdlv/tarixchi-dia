# PDF Document Image Analysis Flask App for Tarixchi

This Flask application provides a RESTful API to extract text blocks from PDF files and highlight the layout elements within PDF documents. It leverages `layoutparser` for document layout analysis and `PyMuPDF` along with `Tesseract OCR` for processing PDF files and extracting text.

## Features

- **Extract Text Blocks:** Analyze PDF files to identify and extract text blocks, returning detailed information about each text block's content and position.
- **Highlight PDF Layouts:** Generate a new PDF file with highlighted layout elements, such as text blocks, tables, and figures, identified in the original PDF.

## Installation

### Pre-requisites

Before setting up the project, ensure you have the following installed:

- Python 3.8 or newer
- Pip (Python package manager)
- [Poppler-utils](https://poppler.freedesktop.org/) for PDF to image conversion
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for Optical Character Recognition

### Setup

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd path-to-repository
```

Install the required Python dependencies:
```
pip install -r requirements.txt
```

### Usage

To start the Flask server:
```
python app.py
```
