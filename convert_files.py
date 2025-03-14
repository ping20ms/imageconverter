from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_files():
    files = request.files.getlist("files")
    saved_files = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            saved_files.append(filename)

    return jsonify({"files": saved_files})

@app.route("/delete-file", methods=["POST"])
def delete_file():
    filename = request.json.get("filename")
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": True})

    return jsonify({"success": False, "error": "File not found"}), 404

@app.route("/convert", methods=["POST"])
def convert_files():
    format_to = request.form.get("format")  # Desired format (e.g., "png")
    converted_files = []

    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if allowed_file(filename):
            img = Image.open(file_path)
            new_filename = os.path.splitext(filename)[0] + f".{format_to}"
            new_file_path = os.path.join(CONVERTED_FOLDER, new_filename)
            img.save(new_file_path, format=format_to.upper())
            converted_files.append(new_filename)

    return jsonify({"converted_files": converted_files})

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(CONVERTED_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
