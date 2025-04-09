from flask import Blueprint, jsonify,request
from utils.mainPage.add_rss import add_rss

bp = Blueprint('rss', __name__)

@bp.route('/rss', methods=["POST"])
def add_rss_handler():
    data = request.get_json()
    rss_address = data['rss_address']
    entries = add_rss(rss_address)
    return jsonify({"success": "500", "entries": entries})

