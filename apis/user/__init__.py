from flask import Blueprint
from flask_restful import Api
from apis.user.views import UserLogin, UserRegister, GetCode, UserQuery, UserOperate

user_api_bp = Blueprint('user', __name__)
user = Api(user_api_bp)
# 用户
user.add_resource(UserLogin, '/user/login/')  # 用户登陆
user.add_resource(UserRegister, '/user/register/')  # 用户注册
user.add_resource(UserQuery, '/user/list/')  # 用户查询
user.add_resource(GetCode, '/user/get_code/')  # 获取验证码
user.add_resource(UserOperate, '/user/operate/')  # 恢复用户

_load_api = True