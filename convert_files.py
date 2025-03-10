from flask import Flask, request, render_template, send_file
from PIL import Image
import pillow_heif
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_image(input_path, output_path):
    """ Converts HEIC, HEIF, PNG images to JPG and saves to output folder """
    try:
        if input_path.lower().endswith((".heic", ".heif")):
            heif_image = pillow_heif.open_heif(input_path)
            img = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
        else:
            img = Image.open(input_path)

        img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=100)  # Max quality to retain file size
        return output_path
    except Exception as e:
        return str(e)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploaded_files = request.files.getlist("file")
        converted_files = []

        for file in uploaded_files[:100]:  # Process up to 100 files
            if file.filename == "":
                continue

            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_filename = os.path.splitext(file.filename)[0] + ".jpg"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            file.save(input_path)  # Save uploaded file
            converted_path = convert_image(input_path, output_path)  # Convert image

            if os.path.exists(converted_path):
                converted_files.append(output_filename)

        return render_template("result.html", files=converted_files)

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(debug=True)
