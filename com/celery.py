from __future__ import absolute_import
from celery import Celery
from com.celery_config import ExchangeDict
# 定义Celery对象
APP_CELERY = Celery()
# Celery配置
APP_CELERY.config_from_object("com.celery_config")


# 未注册的异步任务发送
def send_task(func_path=None, exchange=None, routing_key=None, kwargs=None):
    APP_CELERY.send_task(
        func_path,
        exchange=ExchangeDict.get(exchange),
        routing_key=routing_key,
        kwargs=kwargs,
        eta=None
    )
