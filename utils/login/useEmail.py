import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 配置信息集中管理
EMAIL_CONFIG = {
    'from_addr': '1738978509@qq.com',
    'password': 'agptnizcaqlkegfg',
    'smtp_server': 'smtp.qq.com',
    'port': 465
}

def generate_verification(length=6) -> str:
    return ''.join(random.choices('0123456789', k=length))

def get_email_template(code: str) -> str:
    return f"""
    <div class="verification-box">
        <h1 class="title">小哆啦阅读器</h1>
        <div class="verification-code">{code}</div>
        <p class="tip">验证码5分钟内有效<br>请及时完成验证</p>
    </div>
    <style>
        .verification-box {{
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem 3rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            text-align: center;
            width: 90%;
            max-width: 380px;
        }}
        .title {{
            color: #2c3e50;
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            font-weight: bold;
            letter-spacing: 2px;
        }}
        .verification-code {{
            font-size: 2.5rem;
            letter-spacing: 8px;
            margin: 1.5rem 0;
            color: #3498db;
            font-weight: bold;
            animation: scale 1s ease-in-out infinite alternate;
        }}
        .tip {{
            color: #7f8c8d;
            font-size: 0.9rem;
            margin-top: 1rem;
            line-height: 1.5;
        }}
        @keyframes scale {{
            from {{
                transform: scale(0.95);
            }}
            to {{
                transform: scale(1.05);
            }}
        }}
    </style>
    """

def send_verification_email(to_addr: str) -> str:
    code = generate_verification()
    try:
        msg = MIMEMultipart()
        msg['From'] = f'"Doraemon-Reader" <{EMAIL_CONFIG["from_addr"]}>'
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('小哆啦阅读器验证码', 'utf-8')
        msg.attach(MIMEText(get_email_template(code), 'html', 'utf-8'))

        with smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['port']) as server:
            server.login(EMAIL_CONFIG['from_addr'], EMAIL_CONFIG['password'])
            server.sendmail(EMAIL_CONFIG['from_addr'], to_addr, msg.as_string())

    finally:
            return code

# 使用示例
if __name__ == "__main__":
    try:
        sent_code = send_verification_email('1738978509@qq.com')
        print(f"验证码 {sent_code} 已发送成功")
    except RuntimeError as e:
        print(f"发送失败: {str(e)}")