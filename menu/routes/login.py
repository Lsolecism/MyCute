from datetime import datetime

from flask import session, request, Blueprint

from mycutedb.exist_method import check_email
from mycutedb.get_method import get_user, get_user_password
from utils.login.hashPwd import verify_password
from utils.login.useEmail import send_verification_email

bp = Blueprint('login', __name__)

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
    elif action == "getUser":
        return handle_getUser(data)
    else:
        return {"success": "400", "msg": "无效操作"}


def handle_getUser(data):
    email = data['Email']
    print(get_user(email))
    return {
        "success": "200",
        "user": get_user(email)
    }

def handle_verification(data):
    try:
        email = data['userEmail']
        if not check_email(email):
            return {"success": "500", "msg": "不存在该邮箱"}

        code = send_verification_email(email)
        session[email] = code
        session[f'{email}_expire'] = datetime.now().timestamp() + 300
        return {"success": "200", "msg": "验证码发送成功"}
    except Exception as e:
        print(e)
        return {"success": "400", "msg": e}


def handle_login_verification(data):
    email = data['userEmail']
    user_code = data['verification']

    if datetime.now().timestamp() > session.get(f'{email}_expire', 0):
        return {"success": "400", "msg": "验证码已过期"}

    if session.get(email) != user_code:
        return {"success": "400", "msg": "验证码错误"}

    session.pop(email)
    session.pop(f'{email}_expire')

    user = get_user(email)

    return {
        "success": "500",
        "user": user
    }


def handle_password_login(data):
    email = data['userEmail']
    password = data['password']

    if not check_email(email):
        return {"success": "200", "msg": "不存在该邮箱"}

    if verify_password(password, get_user_password(email)):
        return {
            "success": "500",
            "user": get_user(email)
        }
    else:
        return {"success": "400", "msg": "密码错误"}

