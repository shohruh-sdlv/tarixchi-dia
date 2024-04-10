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


if __name__ == '__main__':
    app.run(port=8000, debug=True)
