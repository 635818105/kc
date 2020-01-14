import time
import logging
import traceback

from flask_cors import CORS

from libs.pool_db import db
from libs.utils.ajax import json_fail
from libs.utils import auth_token
from flask import Flask, Blueprint, make_response
from flask import request
from config import Setting
log = logging.getLogger(__name__)
# CSRF
# Flask实例
app = None


def create_app(config=None):
    """
    说明：创建flask应用
    ----------------------------------------
    修改人          修改日期          修改原因
    ----------------------------------------
    Zuyong Du         2018-10-2
    ----------------------------------------
    """
    global app
    global socketio
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # 设置参数
    # 使用默认配置
    app.config.from_object(Setting)
    # 更新配置
    app.config.from_object(config)
    # 蓝图注册
    configure_blueprints(app)
    app.before_request(cross_domain_access_before)
    app.before_request(config_before_request)
    app.after_request(update_token)
    app.after_request(cross_domain_access_after)
    app.register_error_handler(Exception, exception_handler)
    app.register_error_handler(404, page_not_found)
    return app


def configure_blueprints(app):
    """
    说明：上下文注册蓝图
    ----------------------------------------
    修改人          修改日期          修改原因
    ----------------------------------------
    Zuyong Du         2018-10-22
    ----------------------------------------
    :param app: app
    """
    api_url_prefix = app.config['API_URL_PREFIX']

    def register_module_bp(model_obj, model_name, suffix_='api', url_prefix_=api_url_prefix):
        """
        注册蓝图
        """
        # 若包模块有标识符__load_app或_load_api且为True，则此模块注册，否则忽略
        load_flag_name = "_load_{}".format(suffix_)
        if not (hasattr(model_obj, load_flag_name) and getattr(model_obj, load_flag_name) is False):
            model_bp_name = "{}_{}_bp".format(model_name, suffix_)
            if hasattr(model_obj, model_bp_name):
                model_bp = getattr(model_obj, model_bp_name)
                if isinstance(model_bp, Blueprint) and model_bp not in app.blueprints:
                    app.register_blueprint(model_bp, url_prefix=url_prefix_)

    # 蓝图注册方式一，自动注册
    import pkgutil
    import importlib
    import apis
    package_path = apis.__path__
    package_name = apis.__name__
    import_error_bps = []
    for _, name, status in pkgutil.iter_modules(package_path):
        try:
            m = importlib.import_module('{0}.{1}'.format(package_name, name))
        except ImportError as e:
            import_error_bps.append((package_name, name))
            app.logger.error(
                "package_path:{}, package_name:{}, model_name:{}, except:{}\n{}, {}".format(
                    package_path, package_name, name, e, _, status))
            continue
        else:
            register_module_bp(m, name, suffix_='api', url_prefix_=api_url_prefix)
    for v in import_error_bps:
        package_name, name = v
        m = importlib.import_module('{0}.{1}'.format(package_name, name))
        register_module_bp(m, name, suffix_='api', url_prefix_=api_url_prefix)


def app_white_list():
    """
    说明：白名单地址，匿名用户可以访问
    ----------------------------------------
    修改人          修改日期          修改原因
    ----------------------------------------
    Zuyong Du         2018-10-22
    ----------------------------------------
    """
    url_list = ['/zm/user/login/', '/zm/user/get_code/']
    return url_list


def cross_domain_access_before():
    """
    说明：跨域请求对OPTIONS请求处理
    ----------------------------------------
    修改人          修改日期          修改原因
    ----------------------------------------
    Zuyong Du         2018-10-22
    ----------------------------------------
    """
    pass
    # if request.method == 'OPTIONS':
    #     response = make_response()
    #     response.headers['Access-Control-Max-Age'] = 24 * 60 * 60
    #     # 请求方式说明
    #     # 1.查询 post--有参数, get--无参数
    #     # 2.添加 put
    #     # 3.更新 patch
    #     # 4.删除 delete
    #     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH'
    #     return response


def cross_domain_access_after(response):
    """
    说明：跨域请求 之后  增加header相关信息
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, W-TOKEN'
    response.headers["Access-Control-Expose-Headers"] = 'Content-Disposition'
    return response


def page_not_found(_):
    """
    说明：404页面
    ----------------------------------------
    修改人          修改日期          修改原因
    ----------------------------------------
    Zuyong Du         2018-10-22
    ----------------------------------------
    """
    r = json_fail(request, message="Page not found")
    r.status_code = 404
    return r


def exception_handler(ex):
    """
    说明:全局异常处理
    ------------------
    添加异常明细处理
    """
    ex = traceback.format_exc()
    log.error(ex)
    return json_fail(request, message='服务器开小差')


def update_token(response):
    """
    续签token(如果token过期)
    """
    if request.method == 'OPTIONS':
        return response
    else:
        # 获取token
        token = request.headers.get("w-token") or request.cookies.get("w-token")
        if token:
            d_token = auth_token.decode_token(token)
            phone_number = d_token["phone_number"] if d_token else ""
            user_id = d_token["user_id"] if d_token else 0
            expire = d_token["expire"] if d_token else 0
            # 如果token过期时间到一半就续签
            if time.time() >= expire - Setting.APP_TOKEN_EXPIRE / 2:
                new_token = auth_token.create_token(phone_number, user_id)
                request.__setattr__("w-token", new_token)
        return response


def config_before_request():
    """
    说明：请求拦截
    ---------------
    修改人
    ---------------
    张栋梁
    ---------------
    """
    setting = Setting()
    if eval(setting.TOKEN_AUTH):
        white_flag = False  # 白名单标识
        for url in app_white_list():
            if request.path.startswith(url):
                white_flag = True
                break
        if not white_flag:
            # 白名单不走token验证
            token = request.headers.get("w-token") or request.cookies.get("w-token")
            print(token)
            # 解析token
            d_token = auth_token.decode_token(token)
            phone_number = d_token["phone_number"] if d_token else ""
            user_id = d_token["user_id"] if d_token else 0
            expire = d_token["expire"] if d_token else 0
            user_data = {}
            if phone_number and user_id and expire:
                user_data = db.default.auth_user.filter(id=user_id).get()
                if not user_data:
                    r = json_fail(request, message="w-token异常")
                    r.status_code = 404
                    return r
                # request添加user属性
                request.user = user_data
                if user_data.status == 1:
                    r = json_fail(request, message="账号已被禁用")
                    r.status_code = 404
                    return r
                # 添加token
                request.__setattr__("w-token", token)
            if not user_data:
                r = json_fail(request, message="请求失败")
                r.status_code = 401
                return r
