from flask import request
# from flask_cache import Cache

# cache_config = {
#     'CACHE_TYPE': 'redis',
#     'CACHE_REDIS_HOST': '114.55.88.84',#'127.0.0.1',
#     'CACHE_REDIS_PORT': '6379',
#     'CACHE_REDIS_DB': '',
#     'CACHE_REDIS_PASSWORD': 'xqd2015!'
# }
# cache = Cache(config=cache_config)

from china_border import app


# cache.init_app(app)

@app.before_request
def before_request():
    if request.blueprint is not None:
        bp = app.blueprints[request.blueprint]
        if bp.jinja_loader is not None:
            newsearchpath = bp.jinja_loader.searchpath + app.jinja_loader.searchpath
            app.jinja_loader.searchpath = newsearchpath
            # 以下为2016-03-11日更新：
            # 如果访问非蓝图模块或蓝图中没有指定template_folder,默认使用app注册时指定的全局template_floder.
        else:
            app.jinja_loader.searchpath = app.jinja_loader.searchpath[-1:]
    else:
        app.jinja_loader.searchpath = app.jinja_loader.searchpath[-1:]
