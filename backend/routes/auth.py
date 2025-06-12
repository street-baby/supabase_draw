from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from models import db, User
from utils.email_util import send_verification_code, verify_code

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/send-code', methods=['POST'])
def send_code():
    """发送邮箱验证码"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'message': '邮箱不能为空'}), 400
    
    success, code = send_verification_code(email)
    
    if success:
        # 在开发环境中，可以返回验证码方便测试
        if current_app.debug:
            return jsonify({
                'message': '验证码发送成功',
                'code': code if current_app.debug else None  # 仅在调试模式返回验证码
            }), 200
        return jsonify({'message': '验证码发送成功'}), 200
    else:
        return jsonify({'message': '验证码发送失败，请稍后再试'}), 500

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    password = data.get('password')
    
    if not all([email, code, password]):
        return jsonify({'message': '请填写所有必填字段'}), 400
    
    # 验证码校验
    if not verify_code(email, code):
        return jsonify({'message': '验证码错误或已过期'}), 400
    
    # 创建新用户
    try:
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': '注册成功',
            'user': user.to_dict()
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': '该邮箱已被注册'}), 409
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"注册失败: {str(e)}")
        return jsonify({'message': '注册失败，请稍后再试'}), 500

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    
    if not all([email, code]):
        return jsonify({'message': '请填写所有必填字段'}), 400
    
    # 验证码校验
    if not verify_code(email, code):
        return jsonify({'message': '验证码错误或已过期'}), 400
    
    # 查找用户
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # 如果用户不存在，则创建新用户（无密码，后续可以设置）
        user = User(email=email)
        db.session.add(user)
    
    # 更新最后登录时间
    user.last_login = datetime.now()
    db.session.commit()
    
    # 生成JWT令牌
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=24)
    )
    
    return jsonify({
        'message': '登录成功',
        'user': user.to_dict(),
        'token': access_token
    }), 200

@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_user_profile():
    """获取当前用户信息"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
        
    return jsonify({
        'user': user.to_dict()
    }), 200