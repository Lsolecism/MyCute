from .login import bp as login_bp
from .rss import bp as rss_bp
from .register import bp as register_bp
from .infowindow import bp as info_bp
from .editwindow import bp as edit_bp
from .exitwindow import bp as exit_bp
from .ratewindow import bp as rate_bp
def register_routes(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(rss_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(info_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(exit_bp)
    app.register_blueprint(rate_bp)

    # 可选：注册其他蓝图
    # from .other import bp as other_bp
    # app.register_blueprint(other_bp)
