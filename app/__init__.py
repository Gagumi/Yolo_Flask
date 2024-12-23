from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # 配置 Flask
    app.config['UPLOAD_FOLDER'] = './app/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为 16MB

    # 注册路由
    from app.routes import main
    app.register_blueprint(main)

    return app
