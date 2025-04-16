from flask import Blueprint, jsonify,request

from mycutedb.get_method import get_user_rss, get_user_id, get_article
from utils.mainPage.add_rss import add_rss

bp = Blueprint('rss', __name__)

@bp.route('/rss', methods=["POST"])
def add_rss_handler():
    data = request.get_json()
    # 前端返回来的userId其实是UID
    email = data['email']
    rss_name = data['rss_name']
    rss_address = data['rss_address']
    entries = add_rss(email,rss_name,rss_address)
    return jsonify({"success": "500", "entries": entries})

@bp.route('/getRssCards',methods=["POST"])
def get_rss_cards():
    data = request.get_json()
    email = data['Email']
    userId = get_user_id(email)
    rss_cards = get_user_rss(userId)

    # 处理每个 RSS 卡片
    for card in rss_cards:
        if 'Articles' in card:
            # 处理每篇文章
            for article in card['Articles']:
                if 'Content' in article:
                    # 移除 Value 键
                    article['Content'].pop('Value', None)
                    # 如果删除后 Content 为空，可删除整个字段
                    if not article['Content']:
                        del article['Content']
    print(rss_cards)
    return jsonify({
        "success": "200",  # 状态码改为200
        "RssCards": rss_cards
    })

@bp.route('/rss/article',methods=["POST"])
def get_rss_article():
    data = request.get_json()
    link = data['Link']
    rssId = data['RssId']
    print(rssId)
    article = get_article(rssId,link)
    print(article)
    return jsonify({"success": "500", "Article": article})
