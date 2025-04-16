from datetime import datetime
from pymongo import MongoClient

# 创建 MongoDB 客户端
client = MongoClient('mongodb://localhost:27017/')  # 替换为你的 MongoDB URI
db = client['mycute']  # 替换为你的数据库名称
users_collection = db['users']  # 替换为你的集合名称
feedback_collection = db['feedback']  # 替换为你的反馈集合名称
rss_collection = db['rss']

def update_user_image(user_id, image_id):
    newAvatarUrl = "http://localhost:5000/image/"+image_id
    users_collection.update_one({'_id': user_id},
    {'$set': {'AvatarURL':newAvatarUrl }})

def update_user_info(user_id, user_info):
    users_collection.update_one({'_id': user_id},
    {'$set': {'AvatarURL':user_info['AvatarURL'],'Name':user_info['Name'],'Email':user_info['Email'], 'Profile':user_info['Profile']}})