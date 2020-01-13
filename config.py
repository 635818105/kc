import os
import simplejson as json


class Setting(object):
    # 当前文件路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 读取项目配置文件
    config_file = os.path.join(BASE_DIR, '.env')
    with open(config_file) as f:
        config = f.read()
        SETTING_CONFIG = json.loads(config)
    # 启动端口
    PORT = SETTING_CONFIG["API_PORT"]
    # 主机
    HOST = SETTING_CONFIG["API_HOST"]
    # 接口前缀
    API_URL_PREFIX = "/zm"
    # 是否启用token验证
    TOKEN_AUTH = SETTING_CONFIG["TOKEN_AUTH"]
    # TOKEN 过期时间默认35天
    APP_TOKEN_EXPIRE = 7 * 24 * 60 * 60 * 5
    SECRET_KEY = '240897'
    DEBUG = SETTING_CONFIG["DEBUG"]
    SESSION_COOKIE_NAME = "w_token"
    # 配置
    FILE_VIEW_URLROOT = SETTING_CONFIG["FILE_VIEW_URLROOT"]
    FILE_UPLOAD_URLROOT = SETTING_CONFIG["FILE_UPLOAD_URLROOT"]
    UPLOAD_FILE_KEY_VALUE = SETTING_CONFIG["FILE_UPLOAD_KEY"]
    FILE_READ_URL = SETTING_CONFIG['FILE_VIEW_URLROOT']
    MAX_CONNECTIONS = 20


class DevelopmentConfig(Setting):
    # 调试模式开关
    DEBUG = Setting.DEBUG
    TESTING = False
