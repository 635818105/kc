import datetime
import json
import re
import time

import requests
from flask_restful import Resource, reqparse
from qiniu import Auth, put_data
from werkzeug.datastructures import FileStorage

from libs.pool_db import db
from libs.pool_db.db import Struct
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
        parser.add_argument("category", type=str, default="")
        parser.add_argument("p_id", type=str, default="")
        args = parser.parse_args()
        offset = (args.page_no - 1) * args.pagesize

        items = db.default.product_info.filter(id__gte=0, status=0).order_by("category_id")
        category = db.default.product_category.filter(id__gte=0)[:]
        category_map = {c.id: c.name for c in category}
        if args.pro_name:
            items = items.filter(name__contains=args.pro_name)
        if args.category:
            items = items.filter(category=args.category)
        if args.p_id:
            items = items.filter(id=args.p_id)
        total = items.count()
        if args.page_no > 0:
            items = items[offset:args.pagesize]
        else:
            items = items[:]

        for item in items:
            item.price = str(item.price)
            item.category = category_map.get(item.category_id, "")
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
        product_list = db.default.product_info.filter(status=0)
        c_data = db.default.product_category.filter(status=0)
        category_map = {c.id: c.name for c in c_data}
        data = Struct()
        for c in c_data:
            data[c.name] = []
        for p in product_list:
            category = category_map.get(p.category_id, "")
            if category:
                data[category].append({"p_id": p.id, "name": p.name, "image_url": p.url, "des": p.description})
        return json_ok(data=data)


class CategoryList(Resource):
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
        parser.add_argument("category_name", type=str, default="")
        args = parser.parse_args()
        items = db.default.product_category.filter(id__gte=0, status=0)[:]
        if args.category_name:
            items = items.filter(name__contains=args.category_name)
        data = []
        for i in items:
            obj = Struct()
            obj.id = i.id
            obj.name = i.name
            obj.add_date = i.add_date
            data.append(obj)
        total = len(items)
        return json_ok(data={'data': items, 'total': total})


class CategoryDelete(Resource):
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
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("id", type=int, required=True, help="参数错误")
        args = parser.parse_args()
        db.default.product_category.filter(id=args.id).update(status=1)
        return json_ok(message="删除成功")


class CategoryAdd(Resource):
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
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("name", type=str, required=True, help="参数错误")
        args = parser.parse_args()
        db.default.product_category.create(name=args.name, add_date=int(time.time()))
        return json_ok(message="添加成功")


class CategoryUpdate(Resource):
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
        args = parser.parse_args()
        args.add_date = int(time.time())
        print(args.id, args.name)
        db.default.product_category.filter(id=args.id).update(name=args.name)
        return json_ok(message="更新成功")


class FileUpload(Resource):
    """
    说明：上传文件
    ----------------------------------------
    修改人          修改日期          修改原因
    ----------------------------------------
    吕建威          2018-02-21
    ----------------------------------------
    备注：
    type:
    1 文件之类 cms_data
    2 图片之类 cms_img
    ----------------------------------------
    2019-3-21 宋国洋  改造文件上传方法
    """

    @staticmethod
    def post():
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("type")
            parser.add_argument("file", type=FileStorage, location="files")
            args = parser.parse_args()
            file_data = args.file
            access_key = "cpeyHwtPxfxAbbw-qE9puxJME3PhtvEmpJ6omkkm"
            secret_key = "ZGaUZws2nVownOvyXgEG5b-yAjpl-IR6ECx4yRaG"
            q = Auth(access_key, secret_key)
            # 要上传的空间
            bucket_name = 'zdl-upload'
            # 生成上传 Token，可以指定过期时间等
            token = q.upload_token(bucket_name, None, 3600)
            ret, info = put_data(token, None, file_data.read())
            if info.status_code == 200:
                # 表示上传成功, 返回文件名
                url = "http://qiniu.adongo.cn/" + ret.get("key")
                return json_ok({"file_url": url})
        except Exception as e:
            print(e, "上传文件失败！")
