from flask import Blueprint, request

from mycutedb.add_method import add_Feedback
from mycutedb.get_method import get_user_id

bp = Blueprint('rate',__name__)

@bp.route('/RSS/Rate', methods=['POST'])
def handleRate():
    # {'action': 'rating', 'rating_value': 2, 'feedback': '达娃大', 'Email': '1738978509@qq.com'}
    data = request.get_json()
    print(data)
    user_id = get_user_id(data.get('Email'))
    try:
        add_Feedback(user_id, data.get('feedback'), data.get('rating_value'))
        return {
            "success": "200"
        }
    except Exception as e:
        return {
            "msg":e
        }