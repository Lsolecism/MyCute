from pymongo import MongoClient

# 创建 MongoDB 客户端
client = MongoClient('mongodb://localhost:27017/')  # 替换为你的 MongoDB URI
db = client['mycute']  # 替换为你的数据库名称
users_collection = db['users']  # 替换为你的集合名称
feedback_collection = db['feedback']  # 替换为你的反馈集合名称
rss_collection = db['rss']

def delete_user(user_id):
    # 删除用户
    users_collection.delete_one({"_id": user_id})
    # 删除用户对应的反馈
    feedback_collection.delete_many({"user_id": user_id})
    # 删除用户对应的RSS源
    rss_collection.delete_many({"user_id": user_id})

def delete_rss(user_id,rss_id):
    users_collection.update_one(
        {"_id":user_id},
        {"$pull": {"RssSubscriptions": rss_id}}
    )
    rss_collection.delete_one({"_id": rss_id})

def delete_Article(rss_id, article_link):
    rss_collection.update_one(
        {"_id": rss_id},
        {"$pull": {"Articles": {"Link": article_link}}}
    )
