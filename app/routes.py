import os
from flask import Blueprint, request, render_template, jsonify, send_from_directory, current_app
from app.utils import run_yolo_inference
import logging

main = Blueprint("main", __name__)

# 首页：上传图片的前端页面
@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# 上传图片并处理
@main.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # 保存文件到 uploads 目录
    filename = file.filename
    filepath = os.path.join("./app/uploads", filename)
    file.save(filepath)

    # 运行 YOLO 推理
    detections, output_filename = run_yolo_inference(filepath)

    return jsonify({"detections": detections, "image": filename})

# 提供检测结果图像文件
@main.route("/uploads/<filename>")
def get_file(filename):
    # 生成绝对路径
    uploads_dir = os.path.abspath(os.path.join(current_app.root_path, "uploads"))
    #print(f"Serving file: {os.path.join(uploads_dir, filename)}")  # 调试日志
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Serving file: {uploads_dir}/{filename}")
    return send_from_directory(uploads_dir, filename)
