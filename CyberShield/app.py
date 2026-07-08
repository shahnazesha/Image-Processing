import base64
import io

from flask import Flask, jsonify, render_template, request
from PIL import Image

from steganography import CyberShieldStego

app = Flask(__name__)
stego = CyberShieldStego()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/capacity', methods=['POST'])
def capacity():
    if 'image' not in request.files or not request.files['image'].filename:
        return jsonify({'error': 'No image provided'}), 400

    img = Image.open(request.files['image'])
    width, height = img.size
    return jsonify({
        'capacity': stego.get_capacity(img),
        'width': width,
        'height': height,
    })


@app.route('/api/hide', methods=['POST'])
def hide():
    if 'image' not in request.files or not request.files['image'].filename:
        return jsonify({'error': 'Image is required'}), 400
    if not request.form.get('password'):
        return jsonify({'error': 'Password is required'}), 400
    if not request.form.get('message'):
        return jsonify({'error': 'Message is required'}), 400

    image_file = request.files['image']
    password = request.form['password']
    message = request.form['message']
    raw_bytes = image_file.read()

    try:
        result = stego.hide(raw_bytes, message, password)
        encoded = base64.b64encode(result).decode('utf-8')
        return jsonify({'success': True, 'image': encoded})
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception:
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/api/extract', methods=['POST'])
def extract():
    if 'image' not in request.files or not request.files['image'].filename:
        return jsonify({'error': 'Decryption failed. Wrong password or no hidden data.'}), 400
    if not request.form.get('password'):
        return jsonify({'error': 'Decryption failed. Wrong password or no hidden data.'}), 400

    image_file = request.files['image']
    password = request.form['password']
    raw_bytes = image_file.read()

    try:
        message = stego.extract(raw_bytes, password)
        return jsonify({'success': True, 'message': message})
    except Exception:
        return jsonify({'error': 'Decryption failed. Wrong password or no hidden data.'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
