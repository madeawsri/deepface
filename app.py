from flask import Flask, jsonify, request
from deepface import DeepFace
import os

app = Flask(__name__)

# สร้างโฟลเดอร์สำหรับเก็บภาพอัปโหลด
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to DeepFace API!"})

@app.route('/api/v1/detect', methods=['POST'])
def detect_face():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    # รับไฟล์ภาพ
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        # ใช้ DeepFace ตรวจสอบใบหน้า
        analysis = DeepFace.analyze(img_path=filepath, actions=['age', 'gender', 'emotion'])
        os.remove(filepath)  # ลบไฟล์หลังจากประมวลผล
        return jsonify({"status": "success", "analysis": analysis})
    except Exception as e:
        os.remove(filepath)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
