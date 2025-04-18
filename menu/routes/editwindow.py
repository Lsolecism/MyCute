from concurrent.futures import ThreadPoolExecutor

import requests
from flask import Blueprint, current_app
from pymongo import MongoClient, UpdateOne
from apscheduler.schedulers.background import BackgroundScheduler

bp = Blueprint('edit', __name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['mycute']
rss_source_collection = db['RSS_Source']

if rss_source_collection.count_documents({}) == 0:
    initial_data = [
    {
        "URL": "https://rsshub.app/",
        "State": ""
    },
    {
        "URL":"https://rsshub.rssforever.com/",
        "State":""
    },
    {
        "URL":"https://hub.slarker.me/",
        "State":""
    },
    {
        "URL":"https://rsshub.rss.tips/",
        "State":""
    },
    {
        "URL":"https://rsshub.pseudoyu.com/",
        "State":""
    },
    {
        "URL":"https://rsshub.ktachibana.party/",
        "State":""
    },
    {
        "URL":"https://rsshub.woodland.cafe/",
        "State":""
    }
]
    rss_source_collection.insert_many(initial_data)


def update_status_task():
    def check_url(item):
        try:
            response = requests.get(item["URL"], timeout=5,
                                    headers={'User-Agent': 'Mozilla/5.0'})
            return str(response.status_code)
        except Exception as e:
            return f"Error: {str(e)}"

    all_records = list(rss_source_collection.find({}, {'_id': 1, 'URL': 1}))

    # 批量更新操作
    update_operations = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for record, status in zip(
                all_records,
                executor.map(check_url, all_records)
        ):
            update_operations.append(
                UpdateOne(
                    {'_id': record['_id']},
                    {'$set': {'State': status}}
                )
            )

    # 批量写入更新
    if update_operations:
        rss_source_collection.bulk_write(update_operations)
    current_app.logger.info(f"Updated {len(update_operations)} records")

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=update_status_task,
    trigger='cron',
    hour=3,
    timezone='Asia/Shanghai'
)
scheduler.start()

@bp.route('/RSS/Edit', methods=['GET'])
def get_rss():
    update_status_task()
    return [{
        "URL": item["URL"],
        "State": item.get("State", "")
    } for item in rss_source_collection.find({}, {'_id': 0})]