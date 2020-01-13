import time

from flask_restful import Resource, reqparse

from libs.pool_db import db
from libs.utils.ajax import json_ok


class ProductList(Resource):
    """
    说明：产品列表
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-07
    --------------------------
    """

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("pagesize", type=int, default=20, help="每页记录数")
        parser.add_argument("page_no", type=int, default=1, help="确少分页参数")
        parser.add_argument("pro_name", type=str, default="")
        args = parser.parse_args()
        offset = (args.page_no - 1) * args.pagesize

        items = db.default.product_info.filter(id__gte=0, status=0).order_by("-id")
        category = db.default.product_category.filter(id__gte=0)[:]
        series = db.default.product_series.filter(id__gte=0)[:]
        category_map = {c.id: c.name for c in category}
        series_map = {s.id: s.name for s in series}
        if args.pro_name:
            print(args.pro_name)
            items = items.filter(name__contains=args.pro_name)
        print(items[:])
        total = items.count()
        if args.page_no > 0:
            items = items[offset:args.pagesize]
        else:
            items = items[:]

        for item in items:
            item.price = str(item.price)
            item.category = category_map.get(item.category_id, "")
            item.series = series_map.get(item.series_id, "")

        return json_ok(data={'data': items, 'total': total})


class ProductAdd(Resource):
    """
    说明：产品添加
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-07
    --------------------------
    """

    @staticmethod
    def post():
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("name", type=str, required=True, help="请填写商品名称")
        parser.add_argument("price", type=float, required=True, help="请填写商品金额")
        parser.add_argument("url", type=str, required=True, help="请填写商品图片")
        parser.add_argument("category_id", type=int, default=0, help="请填写商品类型")
        parser.add_argument("description", type=str, required=True, help="请填写商品信息")
        parser.add_argument("series_id", type=int, required=True, help="请填写商品系列")
        args = parser.parse_args()
        args.add_date = int(time.time())

        if db.default.product_info.filter(name=args.name).exists():
            return json_ok(message=f"商品 {args.name} 已存在")

        db.default.product_info.create(**args)
        return json_ok(message="添加成功")


class ProductDel(Resource):
    """
    说明：产品删除
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-07
    --------------------------
    """

    @staticmethod
    def post():
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("id", type=int, required=True, help="参数错误")
        args = parser.parse_args()
        db.default.product_info.filter(id=args.id).update(status=1)
        return json_ok(message="删除成功")


class ProductUpdate(Resource):
    """
    说明：产品修改
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-07
    --------------------------
    """

    @staticmethod
    def post():
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("id", type=int, required=True, help="参数错误")
        parser.add_argument("name", type=str, required=True, help="请填写商品名称")
        parser.add_argument("price", type=float, required=True, help="请填写商品金额")
        parser.add_argument("url", type=str, required=True, help="请填写商品图片地址")
        parser.add_argument("category_id", type=int, default=0, help="请填写商品类型")
        parser.add_argument("description", type=str, required=True, help="请填写商品信息")
        parser.add_argument("series_id", type=int, required=True, help="请填写商品系列")
        args = parser.parse_args()
        args.add_date = int(time.time())

        db.default.product_info.filter(id=args.id).update(**args)
        return json_ok(message="更新成功")


class CategorySeries(Resource):
    """
    说明：产品类别
    --------------------------
    编写人          日期
    --------------------------
    张栋梁          2020-10-07
    --------------------------
    """
    @staticmethod
    def get():
        c_list = db.default.product_category.filter(id__gt=0)[:]
        s_list = db.default.product_series.filter(id__gt=0)[:]
        return json_ok(data={"c_list": c_list, "s_list": s_list})
