IUM | N9 Backend Service

Backend API for IUM/N9 web tools.

Endpoints

1. Image to PDF

URL: /api/img-to-pdf

Method: POST

Body: files (multipart/form-data)

2. Create ZIP

URL: /api/create-zip

Method: POST

Body: files (multipart/form-data)

3. Merge PDF

URL: /api/merge-pdf

Method: POST

Body: files (multipart/form-data)

4. Split PDF

URL: /api/split-pdf

Method: POST

Body: file (multipart/form-data)

Deployment

Requires Python 3.x.
Install dependencies:
pip install -r requirements.txt

Run with Gunicorn:
gunicorn app:app
