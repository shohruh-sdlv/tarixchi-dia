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

if __name__ == '__main__':
    app.run(port=8000, debug=True)
