from bson import Binary, ObjectId
from flask import Blueprint, request, Response, jsonify
from pymongo import MongoClient

from mycutedb.get_method import get_user_id
from mycutedb.update_methods import update_user_info

bp = Blueprint('info', __name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mycute']  # 替换为你的数据库名称
images_collection = db['images']

@bp.route('/updateInfo', methods=['POST'])
def update_info():
    data = request.get_json()
    Email = data['Email']
    user_id = get_user_id(Email)
    update_user_info(user_id, data['newUserInfo'])
    return {"success": "200"}


@bp.route('/uploadImage', methods=['POST'])
def upload_image():
    print("Received request:", request.files)
    if 'file' not in request.files:
        print("No file uploaded")
        return {'error': '未上传文件'}, 400
    file = request.files['file']
    print("Received file:", file.filename)
    if file.filename == '':
        print("Invalid file name")
        return {'error': '无效文件名'}, 400
    # 将文件数据转为二进制
    file_data = Binary(file.read())
    content_type = file.content_type
    # 存储到数据库
    image_doc = {
        'filename': file.filename,
        'contentType': content_type,
        'data': file_data
    }
    result = images_collection.insert_one(image_doc)
    image_id = str(result.inserted_id)
    # 这时候还不能保存到数据库中，因为用户在前端还没有点击保存
    return jsonify({'imageId': image_id, 'success': '200'})


@bp.route('/image/<string:imageId>', methods=['GET'])
def get_image(imageId):
    print("Received imageId:", imageId)  # 现在可以正常打印
    try:
        obj_id = ObjectId(imageId)
    except:
        return {'error': '无效的ID'}, 400

    image = images_collection.find_one({'_id': obj_id})
    if not image:
        return {'error': '图片未找到'}, 404
    return Response(image['data'], mimetype=image['contentType'])