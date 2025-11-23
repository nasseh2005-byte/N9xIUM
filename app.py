import io
import os
import zipfile
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "IUM | N9 Backend",
        "version": "1.0.0"
    })

@app.route('/api/img-to-pdf', methods=['POST'])
def img_to_pdf():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files uploaded"}), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({"error": "No files selected"}), 400

        image_list = []
        for file in files:
            img = Image.open(file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            image_list.append(img)

        if not image_list:
            return jsonify({"error": "Invalid images"}), 400

        output_buffer = io.BytesIO()
        image_list[0].save(
            output_buffer, 
            save_all=True, 
            append_images=image_list[1:], 
            format='PDF'
        )
        output_buffer.seek(0)

        return send_file(
            output_buffer,
            as_attachment=True,
            download_name='converted.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create-zip', methods=['POST'])
def create_zip():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files uploaded"}), 400

        files = request.files.getlist('files')
        output_buffer = io.BytesIO()

        with zipfile.ZipFile(output_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                zip_file.writestr(file.filename, file.read())
        
        output_buffer.seek(0)

        return send_file(
            output_buffer,
            as_attachment=True,
            download_name='archive.zip',
            mimetype='application/zip'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/merge-pdf', methods=['POST'])
def merge_pdf():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files uploaded"}), 400

        files = request.files.getlist('files')
        merger = PdfMerger()

        for file in files:
            merger.append(file)

        output_buffer = io.BytesIO()
        merger.write(output_buffer)
        merger.close()
        output_buffer.seek(0)

        return send_file(
            output_buffer,
            as_attachment=True,
            download_name='merged.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/split-pdf', methods=['POST'])
def split_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        pdf = PdfReader(file)
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, page in enumerate(pdf.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                pdf_bytes = io.BytesIO()
                writer.write(pdf_bytes)
                pdf_bytes.seek(0)
                
                zip_file.writestr(f"page_{i+1}.pdf", pdf_bytes.read())

        zip_buffer.seek(0)

        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name='split_pages.zip',
            mimetype='application/zip'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
