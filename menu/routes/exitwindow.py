from flask import Blueprint, request
from pymongo import MongoClient

from mycutedb.get_method import get_user_id, get_rss_id

bp = Blueprint('exit', __name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mycute']

#       body: JSON.stringify({action:'logout',Email:localStorage.getItem('Email'),
#         saveData:useCategoryStore().filterReadItems()})})
#     fetch('http://localhost:5000/save)

@bp.route('/exit/save', methods=['POST'])
def save_data():
    data = request.get_json()
    print(data)
    # {'action': 'logout', 'Email': '1738978509@qq.com',
    # 'saveData': {'1': {'Id': 1, 'Name': '帕鲁', 'RssUrl': 'https://diygod.cc/feed',
    # 'Items': ['https://xlog.app/api/redirection?characterId=10&noteId=2532',
    # 'https://xlog.app/api/redirection?characterId=10&noteId=2510']}}}
    # 这个是用户的订阅数组的uid，现在我需要根据这个数组和上面的Id做index匹配
    # [ObjectId('67f8f7dd47cccd3263cec15c')]
    Email = data['Email']
    user_id = get_user_id(Email)
    rss_ids = get_rss_id(user_id)
    for key, feed in data.get('saveData', {}).items():
        try:
            feed_id = int(feed['Id']) - 1  # 转换为0-based索引
            if 0 <= feed_id < len(rss_ids):
                rss_id = rss_ids[feed_id]
                items_to_mark_as_read = feed.get('Items', [])

                # 更新对应RSS文档中的Articles数组
                db.rss.update_one(
                    {'_id': rss_id},
                    {'$set': {'Articles.$[elem].IsReaded': True}},
                    array_filters=[{'elem.Link': {'$in': items_to_mark_as_read}}]
                )
        except (ValueError, KeyError) as e:
            print(f"Error processing feed {key}: {str(e)}")
    return {
        "success": "200"
    }

@bp.route('/exit/save/Beacon', methods=['POST'])
def save_data_beacon():
    data = request.get_json()
    Email = data.get('Email')
    if not Email:
        return {"error": "Missing Email"}, 400

    user_id = get_user_id(Email)
    if not user_id:
        return {"error": "User not found"}, 404

    rss_ids = get_rss_id(user_id)
    save_data = data.get('saveData', {})

    for key, feed in save_data.items():
        try:
            feed_id = int(feed['Id']) - 1  # 保持与前端一致的索引逻辑
            if 0 <= feed_id < len(rss_ids):
                rss_id = rss_ids[feed_id]
                items_to_mark = feed.get('Items', [])

                # 批量更新已读状态
                db.rss.update_many(
                    {'_id': rss_id, 'Articles.Link': {'$in': items_to_mark}},
                    {'$set': {'Articles.$[elem].IsReaded': True}},
                    array_filters=[{'elem.Link': {'$in': items_to_mark}}]
                )
        except (ValueError, KeyError) as e:
            print(f"处理订阅源 {key} 时出错: {str(e)}")

    # Beacon 不需要返回 body，但建议返回 204 状态码
    return '', 204