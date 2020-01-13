# Celery远程任务发送,只需要做简单的配置即可
from kombu import Exchange
from config import Setting
# Celery4版本后,CELERY_BROKER_URL改为BROKER_URL
BROKER_URL = f"amqp://{Setting.RQ_NAME}:{Setting.RQ_PASS}@{Setting.RQ_HOST}:{Setting.RQ_PORT}"
# 重连-心跳检测
# BROKER_HEARTBEAT = 10
# 任务发送失败重试,必须结合使用
# CELERY_TASK_PUBLISH_RETRY_POLICY = True
# 任务未响应,将任务交给其它worker执行
CELERY_DISABLE_RATE_LIMITS = True
# 设置默认不存结果
CELERY_TASK_IGNORE_RESULT = True
# 当worker进程意外退出时，task会被放回到队列中(警告：启用此功能可能会导致错误消息循环执行)，默认是False
TASK_REJECT_ON_WORKER_LOST = True
# 只有当worker完成了这个task时，任务才被标记为ack状态
CELERY_ACKS_LATE = True
# celery与broker的连接池连接数
BROKER_POOL_LIMIT = 10
# 链接断开重试
BROKER_CONNECTION_RETRY = True
# 任务序列化和反序列化方案,使用json
CELERY_TASK_SERIALIZER = 'json'
# 指定时区，不指定默认为 'UTC'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
# 默认的队列，如果一个消息不符合其他的队列就会放在默认队列里面
CELERY_TASK_DEFAULT_QUEUE = 'default'
# 默认的路由键是default.default，这个路由键符合上面的default队列
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default.default'

# 定义celery交换机
ExchangeDict = {
    "default_exchange" or "": Exchange('sh_default', type='topic'),  # 默认交换机
    "cms_batch_open": Exchange("cms_batch_open", type="direct"),     # 批量开通学科
    "cms_cancel_match": Exchange("cms_cancel_match", type="direct"),  # 批量退订学科
}
