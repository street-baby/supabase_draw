from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, User, GeneratedImage

# 创建蓝图
image_bp = Blueprint('image', __name__)

@image_bp.route('/api/image/generate', methods=['POST'])
@jwt_required()
def generate_image():
    """生成图像API"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': '用户不存在或未登录'}), 401
    
    data = request.get_json()
    prompt = data.get('prompt')
    style = data.get('style', '自然风格')
    ratio = data.get('ratio', '1:1')
    
    if not prompt:
        return jsonify({'message': '提示词不能为空'}), 400
    
    # 这里应该调用实际的文生图API
    # 为了演示，我们使用一个模拟URL
    image_url = f"https://picsum.photos/seed/{hash(prompt)}/800/800"
    
    # 保存到数据库
    new_image = GeneratedImage(
        user_id=current_user_id,
        prompt=prompt,
        image_url=image_url,
        style=style,
        ratio=ratio
    )
    
    db.session.add(new_image)
    db.session.commit()
    
    return jsonify({
        'message': '图像生成成功',
        'image': new_image.to_dict()
    }), 201

@image_bp.route('/api/image/list', methods=['GET'])
@jwt_required()
def list_images():
    """获取用户生成的图像列表"""
    current_user_id = get_jwt_identity()
    
    # 分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 查询用户的图像
    images = GeneratedImage.query.filter_by(user_id=current_user_id)\
        .order_by(GeneratedImage.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'images': [img.to_dict() for img in images.items],
        'total': images.total,
        'pages': images.pages,
        'current_page': page
    }), 200