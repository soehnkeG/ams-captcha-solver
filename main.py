import base64
import cv2
import easyocr
from flask import Flask, request, jsonify, app
from PIL import Image
import io

reader = easyocr.Reader(['en'], gpu=False)
app = Flask(__name__)


@app.route("/solve", methods=['POST'])
def solve():
    print("received request")
    data = request.get_json()
    file = data.get('image')

    if not file:
        return jsonify({'error': 'No image provided'}), 401

    image_bytes = base64.b64decode(file)
    image = io.BytesIO(image_bytes)
    
    try:
        img = Image.open(image)
        img.verify()  # Raises an exception if the image is invalid
    except Exception as e:
        print("Error decoding image:", e)

    results = reader.readtext(image_bytes, allowlist='0123456789')

    # Prepare the extracted text
    text = ''
    for result in results:
        text += result[1] + ' '

    print(f"text is {text}")

    return jsonify({'text': text})


@app.route("/", methods=['GET'])
def root():
    print("RECEIVED REQUEST")
    return jsonify({"message": "Hello World!"})


if __name__ == '__main__':
    app.run(debug=True)
