import datetime
from flask import session, request, Blueprint, jsonify
from utils.login.hashPwd import hash_password
from utils.login.useEmail import send_verification_email
from utils.mainPage.add_rss import add_rss

bp = Blueprint('main', __name__)
def check_email(email):
    # 示例逻辑，实际应用中需要从数据库中查询
    return True
def getPwd(Email):
    return "123"


@bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()

    if data.get('action') == "getVerification":
        email = data['userEmail']
        if check_email(email):
            code = send_verification_email(email)
            # 存储时绑定邮箱+时间戳
            session[email] = code
            session[f'{email}_expire'] = datetime.datetime.now().timestamp() + 300  # 5分钟过期
            return {"success": "500", "msg": "验证码发送成功"}
        else:
            return {"success": "200", "msg": "不存在该邮箱"}

    if data.get('action') == "loginVerification":
        email = data['userEmail']
        user_code = data['verification']
        # 验证逻辑
        if datetime.datetime.now().timestamp() > session.get(f'{email}_expire', 0):
            return {"success": "400", "msg": "验证码已过期"}

        if session.get(email) == user_code:
            session.pop(email)  # 验证后立即清除
            session.pop(f'{email}_expire')
            # 返回的看前端        setUserInfo(user) {
            #             this.avatar = user.avatar;
            #             this.userId = user.userId;
            #             this.username = user.username;
            #         },user是一个对象，这里需要数据库查询
            return {"success": "500", "user":{"avatar":"https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png","userId":"100001","username":"陈苡於"},
                    "rssSource": "https://rsshub.app"}

    if data.get('action') == "login":
        email = data['userEmail']
        original_password = data['password']
        if not check_email(email):
            return {"success": "200", "msg": "不存在该邮箱"}
        #从数据库中通过email找到用户得到密码哈希值
        hashed_value = getPwd(email)
        # if verify_password(original_password, hashed_value):
        # 这是个桩
        if hashed_value:
            return {"success": "500", "user":{"avatar":"https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png","userId":"100001","username":"陈苡於"},
                    "rssSource": "https://rsshub.app"}
        else:
            return {"success": "400", "msg": "密码错误"}

    if data.get('action') == "register":
        email = data['userEmail']
        if check_email(email):
            return {"success": "200", "msg": "邮箱已存在"}
        password = data['password']
        hash_password(password)
        username = data['username']
        # 将注册写入数据库
        return {"success": "500", "msg": "注册成功"}

@bp.route('/rss', methods=["POST"])
def addRss():
    data = request.get_json()
    rssAddress = data['rss_address']
    entries=add_rss(rssAddress)
    return jsonify({"success": "500", "entries": entries})
