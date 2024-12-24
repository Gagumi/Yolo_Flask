# 使用轻量级 Python 基础镜像
FROM python:3.10-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1  
# 防止 Python 写入 pyc 文件
ENV PYTHONUNBUFFERED=1        
# 强制 Python 输出无缓冲，实时显示日志
ENV TORCH_HOME=/app/.torch    
# 设置 PyTorch 缓存目录

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制 Python 依赖文件
COPY requirements.txt requirements.txt

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 克隆 YOLOv5 仓库到镜像中
RUN git clone https://github.com/ultralytics/yolov5 /app/yolov5

# 复制应用程序代码
COPY . .

# 设置权限，避免权限问题
RUN chmod -R 777 /app

# 暴露应用程序端口
EXPOSE 5000

# 使用 Gunicorn 启动应用
CMD ["gunicorn", "-w", "4", "--threads", "2", "-b", "0.0.0.0:5000", "run:app"]
