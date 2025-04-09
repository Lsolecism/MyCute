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

