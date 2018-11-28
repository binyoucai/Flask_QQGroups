from flask import Flask

from App.settings import envs
from App.views import init_view_router


def create_app(env):
    app = Flask(__name__, template_folder='./templates', static_folder='./static')  # 构建Flask对象

    app.config.from_object(envs.get(env))  # 加载配置

    init_view_router(app)  # 加载view router

    return app
