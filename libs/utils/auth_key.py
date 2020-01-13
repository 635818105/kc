# coding: utf-8
import base64
import time
from config import Setting


def encode_key():
    """
    功能说明: 生成api间认证密匙
    """
    key = '%s%s' % (Setting.PROJECT_KEY, str(int(time.time())))  # 拼接加密key 项目名称+当前时间戳
    return base64.b64encode(str.encode(key))
