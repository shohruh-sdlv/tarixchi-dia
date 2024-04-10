!pip install "detectron2@git+https://github.com/facebookresearch/detectron2.git@v0.5#egg=detectron2"
!pip install "layoutparser[ocr]"
!pip install -U 'git+https://github.com/nikhilweee/iopath'

# Import necessary libraries
import numpy as np
import layoutparser as lp
from PIL import Image
import io
from flask import Flask, request, jsonify, send_file
import fitz  # PyMuPDF

# Initialize the Flask app and the layout model.
app = Flask(__name__)
model = lp.models.Detectron2LayoutModel(
    'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
    label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
)

@app.route('/get-textblocks', methods=['POST'])
def get_textblocks():
    """
    Endpoint to extract text blocks from a PDF file using OCR.
    The PDF file is received as part of the request.
    Returns a JSON response containing detected text blocks.
    """
    # Validate file presence in the request.
    if 'pdf' not in request.files:
        return jsonify({"error": "No pdf file part"}), 400
    file = request.files['pdf']
    
    # Validate file name.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Process valid PDF files only.
    if file and file.filename.lower().endswith('.pdf'):
        try:
            # Open the PDF file and initialize OCR agent.
            doc = fitz.open(stream=file.read(), filetype="pdf")
            page_blocks = []
            ocr_agent = lp.TesseractAgent(languages=request.form.get('language', 'eng'))
            
            # Iterate through each page to detect text blocks.
            for page_num, page in enumerate(doc):
                pix = page.get_pixmap(dpi=300)  # Higher DPI for better image quality.
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = np.asarray(img)
                layout_result = model.detect(img)
                text_blocks = lp.Layout([b for b in layout_result])
                
                # Process each detected block with OCR.
                for block in text_blocks:
                    segment_image = block.pad(left=15, right=15, top=5, bottom=5).crop_image(img)
                    text = ocr_agent.detect(segment_image)
                    block.set(text=text, inplace=True)
                
                # Sort blocks vertically and accumulate results.
                text_blocks = text_blocks.sort(key = lambda b:b.coordinates[1])

                # Save 
                for txt in text_blocks:
                    page_blocks.append({
                        "text": txt.text,
                        "block": str(txt.block),
                        "page": page_num
                    })
            return jsonify(page_blocks)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Invalid file"}), 400

@app.route('/get-pdf', methods=['POST'])
def get_pdf():
    """
    Endpoint to process a PDF file, extract images, analyze layout,
    and return a new PDF with detected layout elements highlighted.
    """
    # Validate file presence in the request.
    if 'pdf' not in request.files:
        return jsonify({"error": "No pdf file part"}), 400
    file = request.files['pdf']
    
    # Validate file name.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Process valid PDF files only.
    if file and file.filename.lower().endswith('.pdf'):
        try:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            images = []
            
            # Process each page to detect and highlight layout elements.
            for page_num, page in enumerate(doc):
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = np.asarray(img)
                layout_result = model.detect(img)
                image = lp.draw_box(img, layout_result, box_width=5, box_alpha=0.2, show_element_type=True, show_element_id=True)
                images.append(image)
            
            # Convert processed images back into a single PDF.
            pdf_bytes_io = convert_to_pdf(images)
            return send_file(pdf_bytes_io, as_attachment=True, attachment_filename='dynamic.pdf', mimetype='application/pdf')
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Invalid file"}), 400

def convert_to_pdf(image_objects):
    """
    Convert a list of PIL Image objects to a PDF and return as a BytesIO object.
    This function takes the processed images, combines them into a single PDF,
    and returns the PDF as a BytesIO stream for sending via Flask.
    """
    pdf_bytes_io = io.BytesIO()
    image_objects[0].save(pdf_bytes_io, format='PDF', save_all=True, append_images=image_objects[1:])
    pdf_bytes_io.seek(0)
    return pdf_bytes_io

if __name__ == '__main__':
    app.run(port=8000, debug=True)

