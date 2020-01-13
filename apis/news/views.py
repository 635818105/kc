from flask_restful import Resource
from libs.utils.ajax import json_ok


class NewsList(Resource):
    """
    说明：新闻列表
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-08
    --------------------------
    """

    @staticmethod
    def get():
        res_data = "hello"
        return json_ok(data=res_data)


class NewsAdd(Resource):
    """
    说明：新闻添加
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-08
    --------------------------
    """
    @staticmethod
    def post():
        return json_ok(message="添加成功")


class NewsDel(Resource):
    """
    说明：新闻删除
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-08
    --------------------------
    """
    @staticmethod
    def post():
        return json_ok(message="删除成功")


class NewsUpdate(Resource):
    """
    说明：新闻修改
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-08
    --------------------------
    """
    @staticmethod
    def post():
        return json_ok(message="更新成功")

