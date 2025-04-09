from flask import Flask
from .config import Config
from .extensions import mongo,cors
from .routes import register_routes  # 新增导入

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # 初始化扩展
    mongo.init_app(app)
    cors.init_app(app)
    # 注册所有路由
    register_routes(app)  # 替换原来的蓝图注册
    return app
