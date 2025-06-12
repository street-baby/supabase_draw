import os

class Config:
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost/douyin_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis配置（用于存储验证码）
    REDIS_URL = 'redis://localhost:6379/0'
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    
    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'  # QQ邮箱服务器
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '1541881974@qq.com'  # 使用环境变量或直接设置
    MAIL_PASSWORD = 'gwsapifjazhzhbeh'  # QQ邮箱授权码，不是登录密码
    MAIL_DEFAULT_SENDER = ('AI文生图平台', '1541881974@qq.com')
    
    # 验证码配置
    CODE_EXPIRE_TIME = 300  # 验证码有效期(秒)