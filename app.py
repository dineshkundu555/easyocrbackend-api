from flask import Flask, request, jsonify
import easyocr
from PIL import Image
import io
import base64
import requests

app = Flask(__name__)
reader = easyocr.Reader(['en'])  # Add 'hi' if Hindi also appears

@app.route('/')
def home():
    return 'EasyOCR API is running!'

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        data = request.get_json()

        if 'image_url' in data:
            response = requests.get(data['image_url'])
            image = Image.open(io.BytesIO(response.content))

        elif 'base64' in data:
            image_data = base64.b64decode(data['base64'])
            image = Image.open(io.BytesIO(image_data))

        else:
            return jsonify({'error': 'No image_url or base64 provided'}), 400

        image = image.convert("RGB")
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)

        result = reader.readtext(image_bytes.read())
        extracted_text = ' '.join([item[1] for item in result])

        return jsonify({'text': extracted_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
