# D:\work_for_python\MyCute\config.py
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()  # 确保.env文件加载


class Config:
    # 安全配置
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))

    # MongoDB配置
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_CONNECT_TIMEOUT_MS = 3000  # 连接超时设置
    MONGO_SOCKET_TIMEOUT_MS = 5000  # 操作超时设置

    # 会话配置（与app.py中的配置合并）
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    SESSION_REFRESH_EACH_REQUEST = True

    # CORS配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    CORS_METHODS = ['GET', 'POST', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    CORS_SUPPORTS_CREDENTIALS = True


# class ProductionConfig(Config):
#     DEBUG = False
#     MONGO_URI = os.getenv('PROD_MONGO_URI')  # 生产环境专用URI


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/mycute'
