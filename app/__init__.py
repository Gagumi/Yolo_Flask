from flask import Flask

def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)
    
    # 配置 Flask
    app.config['UPLOAD_FOLDER'] = './app/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为 16MB

    # 注册蓝图
    from app.routes import main
    app.register_blueprint(main)

    # 注册错误处理（可选）
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return "Uploaded file is too large. Maximum file size is 16MB.", 413

    return app
