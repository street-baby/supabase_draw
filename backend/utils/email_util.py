import random
import string
import redis
import logging
from flask import current_app
from flask_mail import Mail, Message

# 初始化但不立即连接
mail = Mail()
redis_client = None

def init_redis(app):
    """在应用上下文中初始化Redis客户端"""
    global redis_client
    try:
        redis_client = redis.Redis.from_url(app.config['REDIS_URL'])
        # 测试连接
        redis_client.ping()
        app.logger.info("Redis连接成功")
        return redis_client
    except Exception as e:
        app.logger.error(f"Redis连接失败: {str(e)}")
        # 如果连接失败，使用内存字典作为替代
        from collections import defaultdict
        redis_client = MemoryStore()
        app.logger.warning("使用内存存储作为Redis替代")
        return redis_client

class MemoryStore:
    """内存存储，用于在Redis不可用时作为替代"""
    def __init__(self):
        self.store = {}
        self.expire_times = {}
        import threading
        self.lock = threading.Lock()
        
    def setex(self, key, time, value):
        with self.lock:
            self.store[key] = value
            import time as time_module
            self.expire_times[key] = time_module.time() + time
            
    def get(self, key):
        with self.lock:
            if key not in self.store:
                return None
            import time as time_module
            if time_module.time() > self.expire_times.get(key, 0):
                # 已过期
                del self.store[key]
                del self.expire_times[key]
                return None
            return self.store[key]
            
    def delete(self, key):
        with self.lock:
            if key in self.store:
                del self.store[key]
            if key in self.expire_times:
                del self.expire_times[key]

def generate_verification_code(length=6):
    """生成数字验证码"""
    return ''.join(random.choices(string.digits, k=length))

def send_verification_code(to_email):
    """发送验证码到邮箱"""
    code = generate_verification_code()
    
    # 确保redis_client已初始化
    if redis_client is None:
        current_app.logger.error("Redis客户端未初始化")
        return False, None
        
    # 存储验证码到Redis，设置过期时间
    key = f"verification_code:{to_email}"
    try:
        redis_client.setex(key, current_app.config['CODE_EXPIRE_TIME'], code)
    except Exception as e:
        current_app.logger.error(f"存储验证码失败: {str(e)}")
        return False, None
    
    # 发送邮件
    subject = "AI文生图平台 - 邮箱验证码"
    body = f"""
    <h2>AI文生图平台 - 邮箱验证码</h2>
    <p>您好！</p>
    <p>感谢您注册使用AI文生图平台。您的验证码是:</p>
    <h1 style="color:#e67e22;">{code}</h1>
    <p>此验证码在5分钟内有效，请尽快验证。</p>
    <p>如果这不是您本人的操作，请忽略此邮件。</p>
    <p>---</p>
    <p>AI文生图平台团队</p>
    """
    
    try:
        msg = Message(
            subject=subject,
            recipients=[to_email],
            html=body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        # 在开发环境中，如果邮件发送失败，也返回验证码供测试
        if current_app.debug:
            try:
                mail.send(msg)
                current_app.logger.info(f"验证码邮件已发送到 {to_email}")
            except Exception as e:
                current_app.logger.warning(f"开发环境: 邮件发送失败，但仍返回验证码: {str(e)}")
                # 在开发环境返回验证码
                return True, code
            return True, code
        else:
            # 生产环境正常发送
            mail.send(msg)
            return True, None
    except Exception as e:
        current_app.logger.error(f"发送邮件失败: {str(e)}")
        # 清理已存储的验证码
        try:
            redis_client.delete(key)
        except:
            pass
        return False, None

def verify_code(email, code):
    """验证邮箱和验证码是否匹配"""
    if redis_client is None:
        current_app.logger.error("Redis客户端未初始化")
        return False
    
    key = f"verification_code:{email}"
    try:
        stored_code = redis_client.get(key)
        
        if not stored_code:
            return False  # 验证码不存在或已过期
        
        # 如果是bytes类型，需要解码
        if isinstance(stored_code, bytes):
            stored_code = stored_code.decode()
        
        if stored_code == code:
            redis_client.delete(key)  # 验证成功后删除验证码
            return True
        
        return False
    except Exception as e:
        current_app.logger.error(f"验证码验证失败: {str(e)}")
        return False