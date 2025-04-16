from flask import  request, Blueprint
from mycutedb.add_method import add_User
from mycutedb.exist_method import check_email
from mycutedb.get_method import get_user
from utils.login.hashPwd import hash_password

bp = Blueprint('register', __name__)
@bp.route('/register', methods=["POST"])
def handle_registration():
    data = request.get_json()
    print(data)
    email = data['userEmail']
    if check_email(email):
        return {"success": "200", "msg": "邮箱已存在"}
    hashed_value = hash_password(data['password'])
    data['Password'] = hashed_value
    # 默认头像地址
    data['AvatarURL'] = "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
    data['Profile'] = "这个人很懒，什么都没有留下"
    data['RssSource'] = "https://rsshub.app"
    add_User(data)
    # 实际应保存到数据库
    user = get_user(email)
    return {"success": "500", "msg": "注册成功","user":user}