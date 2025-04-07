import os
from init import create_app
from flask_cors import CORS

app = create_app()
app.config['SECRET_KEY'] = os.urandom(24)
app.config.update(
    SESSION_PERMANENT=True,  # 启用持久会话
    PERMANENT_SESSION_LIFETIME=300,  # 5分钟过期
    SESSION_REFRESH_EACH_REQUEST=True  # 每次请求刷新有效期
)

CORS(
    app,
    origins="http://localhost:5173",  # 前端地址
    methods=["GET", "POST", "OPTIONS"],  # 明确允许的HTTP方法
    allow_headers=["Content-Type", "Authorization"],  # 允许的请求头
    supports_credentials=True  # 允许携带Cookie（如果需要）
)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)