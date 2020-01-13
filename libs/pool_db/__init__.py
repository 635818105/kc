import os
import pymysql
import simplejson as json
from .db import Hub

db = Hub(pymysql)
# 当前文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 当前文件上级路径
ENV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# 读取数据库配置文件
config_file = os.path.join(ENV_DIR, '.env')
with open(config_file) as f:
    config = f.read()
    DATABASE_CONFIG = json.loads(config)
DB_WAIT_TIMEOUT = 29  # 单个连接最长维持时间
DB_POOL_SIZE = 8  # 连接池最大连接数
# 数据库字典集合
DATABASES = {
    "default": {
        "DB_NAME": "first_world",
        "DB_HOST": DATABASE_CONFIG["WORLD_BASE_HOST"],
        "DB_USER": DATABASE_CONFIG["WORLD_BASE_USER"],
        "DB_PASS": DATABASE_CONFIG["WORLD_BASE_PASSWORD"],
        "DB_PORT": DATABASE_CONFIG["WORLD_BASE_PORT"],
    }
}

# 初始化db数库链接方式
for table, db_param in DATABASES.items():
    db.add_pool(
        table,
        db=db_param["DB_NAME"],
        host=db_param["DB_HOST"],
        user=db_param["DB_USER"],
        passwd=db_param["DB_PASS"],
        port=int(db_param["DB_PORT"]),
        charset='utf8mb4',
        autocommit=True,
        pool_size=DB_POOL_SIZE,
        wait_timeout=DB_WAIT_TIMEOUT
    )
