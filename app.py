from flask import Flask, request, render_template, send_file
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if not file:
        return 'No file uploaded.', 400

    img = Image.open(file.stream)
    brightness = float(request.form.get('brightness', 1.0))
    contrast = float(request.form.get('contrast', 1.0))
    saturation = float(request.form.get('saturation', 1.0))
    sharpness = float(request.form.get('sharpness', 1.0))

    img = ImageEnhance.Brightness(img).enhance(brightness)

    img = ImageEnhance.Contrast(img).enhance(contrast)

    img = ImageEnhance.Color(img).enhance(saturation)

    img = ImageEnhance.Sharpness(img).enhance(sharpness)

    if img.mode == 'RGBA':
        img = img.convert('RGB')

    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True)
