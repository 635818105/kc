import time
import base64
from config import Setting


def create_check_code(user_id, expire_time):
    """
    快速计算session校验码
    ----------------------
    添加user_id
    """
    return int(user_id) ^ expire_time ^ int(Setting.SECRET_KEY)


def create_token(phone_number, user_id):
    """
    生成session值
    1. 校验码 = 手机号 ^用户ID ^ 过期时间戳 ^ 服务器SECRET_KEY
    2. token = 账户ID|用户ID|过期时间戳|校验码
    3. token = 异或加密(token, 服务器SECRET_KEY)
    4. token = Base64编码(token)
    -------------------------
    添加python3的兼容
    """
    expire_time = int(time.time()) + Setting.APP_TOKEN_EXPIRE
    code = create_check_code(user_id, expire_time)
    token = "%s|%s|%s|%s" % (phone_number, user_id, expire_time, code)
    # 对token进行encode,转换成bytearray可接收的类型
    token = str_xor(token.encode(), int(Setting.SECRET_KEY))
    # 去除base64编码中的等号, 避免cookie带引号
    token = base64.b64encode(token).decode().rstrip("=")
    return token


def decode_token(token):
    """
    解析token, 成功返回{phone_number:手机号, user_id:用户ID, expire:过期时间戳}, 失败返回None
    -----------------------------------------------------------------------------
    在token中添加user_id
    """
    if not token:
        return
    # 填充base64被去掉的等号
    token += '=' * (-len(token) % 4)
    token = base64.b64decode(token)
    token = str_xor(token, int(Setting.SECRET_KEY))
    # 将token转换成str类型
    token = token.decode("utf-8")
    phone_number, user_id, expire_time, code = token.split('|')
    phone_number = phone_number
    user_id = int(user_id)
    expire_time = int(expire_time)
    code = int(code)
    nowt = time.time()
    if nowt > expire_time:
        return
    check_code = create_check_code(user_id, expire_time)
    if code != check_code:
        return
    return {'phone_number': phone_number, 'user_id': user_id, 'expire': expire_time}


def str_xor(s, key):
    """
    功能:异或加密
    返回:一个bytearray类型
    """
    key = key & 0xff
    a = bytearray(s)
    b = bytearray(len(a))
    for i, c in enumerate(a):
        b[i] = c ^ key
    return b
