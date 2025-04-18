from bson import ObjectId

from mycutedb.add_method import users_collection, rss_collection


def get_user(Email):
    user = users_collection.find_one({"Email": Email})
    return user

def get_user_id(Email):
    user = users_collection.find_one({"Email": Email})
    return user["_id"]

def get_user_rss(user_id):
    user = users_collection.find_one({"_id": user_id})
    rss_ids = user["RssSubscriptions"]
    return list(rss_collection.find({"_id": {"$in": rss_ids}}))

def get_user_password(email):
    user = users_collection.find_one({"Email": email})
    return user["Password"]

def get_article(rss_id,link):
    rss = rss_collection.find_one(ObjectId(rss_id))
    if rss is None:
        return None
    print(rss['Articles'])
    print(link)
    for article in rss["Articles"]:
        if article["Link"] == link:
            return article

def get_rss_id(user_id):
    user = users_collection.find_one({"_id": user_id})
    rss_ids = user["RssSubscriptions"]
    return rss_ids