import uuid
from datetime import datetime
from flask import jsonify

def generate_order_number():
    """生成唯一的订单号，例如：YYYYMMDDHHMMSS + 8位随机字符"""
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_part = uuid.uuid4().hex[:8].upper()
    return f"{now}{random_part}"

def api_success(data=None, message=""):
    """生成标准的成功 API 响应"""
    response = {
        "status": "success",
        "message": message,
        "data": data
    }
    return jsonify(response), 200

def api_error(message="", status_code=400):
    """生成标准的失败 API 响应"""
    response = {
        "status": "error",
        "message": message
    }
    return jsonify(response), status_code
