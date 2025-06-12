from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from config import Config
from models import db
from utils.email_util import mail, init_redis
from routes.auth import auth_bp
from routes.image import image_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    # 配置CORS，允许前端跨域请求
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    
    db.init_app(app)
    mail.init_app(app)
    
    # 在应用上下文中初始化Redis
    with app.app_context():
        init_redis(app)
    
    jwt = JWTManager(app)
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(image_bp)
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok'}
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5300)