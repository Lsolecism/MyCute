from datetime import datetime
from pymongo import MongoClient

# 创建 MongoDB 客户端
client = MongoClient('mongodb://localhost:27017/')  # 替换为你的 MongoDB URI
db = client['mycute']  # 替换为你的数据库名称
users_collection = db['users']  # 替换为你的集合名称
feedback_collection = db['feedback']  # 替换为你的反馈集合名称
rss_collection = db['rss']

# 添加计数器集合初始化
if db.counters.find_one({"_id": "users"}) is None:
    db.counters.insert_one({"_id": "users", "seq": 0})

def get_next_sequence():
    counter = db.counters.find_one_and_update(
        {"_id": "users"},
        {"$inc": {"seq": 1}},
        return_document=True
    )
    return f"{counter['seq']:04d}"

# 这里面的user暂时是初始化的，后面需要将这些东西拆开
def add_User(userData):
    uid = get_next_sequence()
    new_user = {
        "name":userData["username"],
        "AvatarURL": userData["AvatarURL"],
        "Email": userData["userEmail"],
        "Password": userData["Password"],
        "RssSource": userData["RssSource"],
        "Profile": userData["Profile"],
        "FeedbackId":[],
        "RssSubscriptions": [],
        "UID": uid,
        "Created_time":datetime.now()
    }
    users_collection.insert_one(new_user)
    return True
def add_Feedback(user_id, feedback, score):
    feedback_doc = {
        "UserId": user_id,
        "Feedback": feedback,
        "Score": score,
        "Date": datetime.now()
    }
    feedback_id =  feedback_collection.insert_one(feedback_doc).inserted_id
    users_collection.update_one(
        {"_id": user_id},
        {"$push": {"Feedback": feedback_id}}
    )
    return True

def add_Rss(user_id, rss_name, rss_url, entries):
    rss_doc = {
        "UserId":user_id,
        "RssName": rss_name,
        "RssUrl": rss_url,
        "Articles": []
    }
    rss_id = rss_collection.insert_one(rss_doc).inserted_id
    add_Article(entries, rss_id)
    users_collection.update_one(
        {"_id": user_id},
        {"$push": {"RssSubscriptions": rss_id}}
    )
    return True

def add_Article(entries,rss_id):
    for entry in entries:
        rss_collection.update_one(
            {"_id": rss_id},
            {"$push": {"Articles": {
                "Title": entry['title'],
                "Description": entry['summary'],
                "Link": entry['link'],
                "Published": entry['published'],
                "Author": entry['author'],
                "Content": {
                    "Value": entry['content'][0].value,
                    "ImageUrl": entry['image_url']
                },
                "IsReaded": False
            }}}
        )

