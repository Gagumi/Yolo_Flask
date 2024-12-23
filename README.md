
# YOLOv5 Flask 项目部署文档

## 项目简介

本项目使用 Flask 框架部署 YOLOv5 模型，并通过 Gunicorn 提供高并发支持，同时利用 Nginx 作为反向代理进行负载均衡。模型可对上传的图片进行目标检测，并将结果以图像和数据的形式返回。

---

## 部署环境

- **操作系统**: Ubuntu 20.04 (部署在阿里云 ECS 实例)
- **Python 版本**: 3.10
- **框架和工具**:
  - Flask
  - Gunicorn
  - Nginx
  - Docker & Docker Compose

---

## 部署步骤

### 1. 克隆项目代码

在本地或服务器上克隆项目代码：
```bash
git clone https://github.com/Gagumi/Yolo_Flask.git
cd YOLO_FLASK
```

### 2. 配置 Docker 环境

#### 安装 Docker 和 Docker Compose

参考官方文档安装 [Docker](https://docs.docker.com/engine/install/) 和 [Docker Compose](https://docs.docker.com/compose/install/)。

验证安装：
```bash
docker --version
docker-compose --version
```

#### 配置 Docker 镜像加速

为提高 Docker 镜像的拉取速度，配置国内镜像加速器：
```bash
sudo nano /etc/docker/daemon.json
```

添加以下内容：
```json
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
```

重启 Docker 服务：
```bash
sudo systemctl restart docker
```

### 3. 构建和启动 Docker 容器

执行以下命令以构建和启动服务：
```bash
docker-compose up -d --build
```

### 4. 访问服务

在浏览器中访问服务器的公网 IP，即可使用上传图片进行目标检测。

---

## 配置文件说明

### Dockerfile

`Dockerfile` 中安装了所需依赖，并使用 Gunicorn 作为 WSGI 服务器，配置如下：
```dockerfile
# 使用轻量级 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 克隆 YOLOv5 仓库
RUN git clone https://github.com/ultralytics/yolov5 /app/yolov5

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["gunicorn", "-w", "4", "--threads", "2", "-b", "0.0.0.0:5000", "run:app"]
```

### Nginx 配置

`nginx.conf` 文件中设置反向代理到 Flask 应用：
```nginx
server {
    listen 80;

    location / {
        proxy_pass http://app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 常见问题及解决方法

### 1. **502 Bad Gateway**
原因：Nginx 无法连接到 Flask 应用。

解决方法：
- 检查 Flask 是否运行正常：
  ```bash
  docker logs yolo_flask-app-1
  ```
- 检查 Nginx 配置文件和 `docker-compose.yml` 文件中网络配置是否正确。

### 2. **模型下载超时或失败**
原因：YOLOv5 模型动态下载超时。

解决方法：
- 在 Dockerfile 中预先克隆 YOLOv5 仓库，并使用 `source='local'` 禁用动态下载。

---

## 高并发支持

### 使用 Gunicorn 提升并发能力

`Gunicorn` 的配置：
- **4 个 Worker**：每个 Worker 处理独立请求。
- **2 个线程**：每个 Worker 内部启用多线程。
- **线程池配置**：支持高并发请求。

命令：
```bash
gunicorn -w 4 --threads 2 -b 0.0.0.0:5000 run:app
```

### Nginx 的负载均衡

通过配置 Nginx 实现多实例负载均衡：
```nginx
upstream flask_servers {
    server app1:5000;
    server app2:5000;
}

server {
    listen 80;

    location / {
        proxy_pass http://flask_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 性能测试

使用 ApacheBench (ab) 测试性能：
```bash
ab -n 1000 -c 50 http://<your-server-ip>/
```

---

## 总结

本项目实现了：
- YOLOv5 模型的 API 部署；
- Gunicorn 支持的高并发应用；
- Nginx 的反向代理和负载均衡配置。

如需改进，可以进一步优化模型加载和缓存机制，提升推理速度和资源利用率。

---

如果有更多问题，欢迎联系！ 😊
