from datetime import datetime
from flask import session, request, Blueprint
from utils.login.useEmail import send_verification_email

bp = Blueprint('login', __name__)


# 临时工具函数（后续应迁移到单独模块）
def check_email(email):
    # 示例逻辑，实际需要数据库查询
    return True


def getPwd(email):
    # 桩函数，实际需要数据库查询
    return "123"


@bp.route('/login', methods=["POST"])
def login_handler():
    data = request.get_json()
    action = data.get('action')

    if action == "getVerification":
        return handle_verification(data)
    elif action == "loginVerification":
        return handle_login_verification(data)
    elif action == "login":
        return handle_password_login(data)
    else:
        return {"success": "400", "msg": "无效操作"}


def handle_verification(data):
    email = data['userEmail']
    if not check_email(email):
        return {"success": "200", "msg": "不存在该邮箱"}

    code = send_verification_email(email)
    session[email] = code
    session[f'{email}_expire'] = datetime.now().timestamp() + 300
    return {"success": "500", "msg": "验证码发送成功"}


def handle_login_verification(data):
    email = data['userEmail']
    user_code = data['verification']

    if datetime.now().timestamp() > session.get(f'{email}_expire', 0):
        return {"success": "400", "msg": "验证码已过期"}

    if session.get(email) != user_code:
        return {"success": "400", "msg": "验证码错误"}

    session.pop(email)
    session.pop(f'{email}_expire')
    return {
        "success": "500",
        "user": {
            "avatar": "https://example.com/avatar.png",
            "userId": "100001",
            "username": "陈苡於"
        },
        "rssSource": "https://rsshub.app"
    }


def handle_password_login(data):
    email = data['userEmail']
    password = data['password']

    if not check_email(email):
        return {"success": "200", "msg": "不存在该邮箱"}

    if not getPwd(email):  # 实际应验证密码哈希
        return {"success": "400", "msg": "密码错误"}

    return {
        "success": "500",
        "user": {
            "avatar": "https://example.com/avatar.png",
            "userId": "100001",
            "username": "陈苡於"
        },
        "rssSource": "https://rsshub.app"
    }

