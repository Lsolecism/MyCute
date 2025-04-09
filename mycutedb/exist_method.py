from pymongo import MongoClient

# 创建 MongoDB 客户端
client = MongoClient('mongodb://localhost:27017/')  # 替换为你的 MongoDB URI
db = client['mycute']  # 替换为你的数据库名称
users_collection = db['users']  # 替换为你的集合名称

def check_email(email):
    # 检查邮箱是否存在
    existing_user = users_collection.find_one({"Email": email})
    if existing_user:
        return True
    else:
        return False