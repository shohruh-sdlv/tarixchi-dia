# Import necessary libraries
import numpy as np
import layoutparser as lp
from PIL import Image
import io
from flask import Flask, request, jsonify, send_file
import fitz  # PyMuPDF

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get-textblocks', methods=['POST'])
def get_textblocks():
    if 'pdf' not in request.files:
        return jsonify({"error": "No pdf file part"}), 400
    # Additional code to process the PDF and extract text blocks...
    return jsonify({"message": "Text blocks extracted"})

@app.route('/get-pdf', methods=['POST'])
def get_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No pdf file part"}), 400
    # Additional code to process the PDF, highlight layouts, and return a new PDF...
    return send_file('path/to/new_pdf', as_attachment=True)

def convert_to_pdf(image_objects):
    pdf_bytes_io = io.BytesIO()
    image_objects[0].save(pdf_bytes_io, format='PDF', save_all=True, append_images=image_objects[1:])
    pdf_bytes_io.seek(0)
    return pdf_bytes_io


if __name__ == '__main__':
    app.run(port=8000, debug=True)
