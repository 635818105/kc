import base64
import random
import time

from flask_restful import Resource, reqparse

from libs.pool_db import db
from libs.utils.ajax import json_ok, json_fail
from libs.utils.auth_token import create_token


class UserLogin(Resource):
    """
    说明：管理员登陆
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-08
    --------------------------
    """

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, help="请输入账号")
        parser.add_argument("password", required=True, help="请输入密码")
        parser.add_argument("code", required=True, help="请输入验证码")
        args = parser.parse_args()
        # 获取参数值
        username = args.username
        password = args.password
        code = args.code
        base64_password = base64.b64encode(password.encode())
        user_data = db.default.auth_user.filter(username=username).get()
        if not user_data:
            return json_fail(message="该账号不存在")
        if user_data.password != base64_password.decode():
            return json_fail(message="账号或密码错误")
        if user_data.status == 1:
            return json_fail(message="该账号已禁用")
        # 验证验证码
        code_data = db.default.get_code_log.filter(phone=user_data.username).order_by('-add_date').get()
        if not code:
            # 验证不存在或过期
            return json_fail(message="验证码不存在,重新获取!")
        elif int(time.time()) - code_data.add_date > 5 * 60:
            return json_fail(message="验证码已过期,点击图片重新获取!")
        elif code == code_data.code:
            token = create_token(user_data.username, user_data.id)
            data = dict(token=token)
            # 更新用户最后登录时间
            db.default.auth_user.filter(id=user_data.id).update(last_login=int(time.time()))
            return json_ok(data=data, message="登录成功")
        else:
            return json_fail(message="手机验证码不正确")


class UserRegister(Resource):
    """
    说明：管理员注册
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-08
    --------------------------
    """

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, default="", required=True)
        parser.add_argument("name", type=str, default="", required=True)
        parser.add_argument("password", type=str, default="", required=True)
        parser.add_argument("t_password", type=str, default="", required=True)
        args = parser.parse_args()
        if args.password != args.t_password:
            return json_fail(message="两次输入的密码不一致")
        user_id = db.default.auth_user.create(
            username=args.username,
            name=args.name,
            add_date=int(time.time()),
            password=base64.b64encode(args.password.encode())
        )
        if user_id:
            return json_ok(message="注册成功")
        else:
            return json_fail(message="请稍后重试")


class UserQuery(Resource):
    """
    说明：管理员查询
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-08
    --------------------------
    """

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("phone", type=str, default="")
        parser.add_argument("name", type=str, default="")
        parser.add_argument("user_id", type=str, default="")
        args = parser.parse_args()
        user = db.default.auth_user.filter()
        if args.phone:
            user = user.filter(username=args.phone)
        if args.name:
            user = user.filter(name=args.name)
        if args.user_id:
            if args.user_id.isdigit():
                user_id = int(args.user_id)
            else:
                return json_fail(message="用户编号应为数字！")
            user = user.filter(id=user_id)
        user_list = user[:]
        for u in user_list:
            if u.status == 0:
                u.status_str = "正常"
            if u.status == 1:
                u.status_str = "禁用"
        return json_ok(data=user_list)


class UserOperate(Resource):
    """
    说明：管理员操作
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-08
    --------------------------
    """

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        args = parser.parse_args()
        user_id = args.user_id
        user = db.default.auth_user.filter(id=user_id).get()
        if user.status == 0:
            db.default.auth_user.filter(id=user_id).update(status=1)
            return json_ok(message="禁用成功")
        if user.status == 1:
            db.default.auth_user.filter(id=user_id).update(status=0)
            return json_ok(message="恢复成功")


class GetCode(Resource):
    """
    说明：生成验证码
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-08
    --------------------------
    """

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("phone", type=str, required=True)
        args = parser.parse_args()
        if not args.phone:
            return json_fail(message="请输入手机号")
        code_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        code = random.sample(code_str, 4)
        code = "".join(code).lower()
        db.default.get_code_log.create(
            code=code,
            add_date=int(time.time()),
            phone=args.phone
        )
        return json_ok(data=code)
