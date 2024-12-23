import sys
import os

# 将 yolov5 目录添加到 Python 搜索路径
sys.path.append(os.path.join(os.getcwd(), 'yolov5'))

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)