from flask import Flask, request, jsonify
import os
from convert_image_to_dxf import convert_image_to_dxf
from convert_dxf_to_3d import convert_dxf_to_3d

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
DXF_FOLDER = "dxf_files"
MODEL_FOLDER = "models"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DXF_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)

@app.route("/upload_image", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    # Convert image to DXF
    dxf_path = os.path.join(DXF_FOLDER, file.filename.replace(".jpg", ".dxf").replace(".jpeg", ".dxf"))
    convert_image_to_dxf(image_path, dxf_path)

    # Convert DXF to 3D Model
    model_path = os.path.join(MODEL_FOLDER, file.filename.replace(".jpg", ".step").replace(".jpeg", ".step"))
    convert_dxf_to_3d(dxf_path, model_path)

    return jsonify({"message": "Conversion successful", "dxf_file": dxf_path, "model_file": model_path})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
