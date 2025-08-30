import uuid
from datetime import datetime
from flask import jsonify


def generate_order_number():
    """
    生成唯一的订单号
    规则：当前 UTC 时间（年月日时分秒）+ 8 位随机大写字符
    例如：20250830123045123ABCD
    """
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")  # 获取当前 UTC 时间并格式化
    random_part = uuid.uuid4().hex[:8].upper()  # 生成 8 位随机大写字符串
    return f"{now}{random_part}"  # 拼接时间和随机部分作为订单号


def api_success(data=None, message=""):
    """
    生成标准的成功 API 响应
    参数:
        data: 返回的数据内容（可选）
        message: 提示信息（可选）
    返回:
        JSON 格式响应，HTTP 状态码 200
    """
    response = {
        "status": "success",  # 状态标识
        "message": message,  # 提示信息
        "data": data,  # 返回数据
    }
    return jsonify(response), 200


def api_error(message="", status_code=400):
    """
    生成标准的失败 API 响应
    参数:
        message: 错误提示信息
        status_code: HTTP 状态码，默认 400
    返回:
        JSON 格式响应，指定 HTTP 状态码
    """
    response = {
        "status": "error",  # 状态标识
        "message": message,  # 错误信息
    }
    return jsonify(response), status_code
