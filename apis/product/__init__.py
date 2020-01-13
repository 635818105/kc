from flask import Blueprint
from flask_restful import Api
from apis.product.views import ProductList, ProductAdd, ProductDel, ProductUpdate, CategorySeries

product_api_bp = Blueprint('product', __name__)
product = Api(product_api_bp)
# 产品
product.add_resource(ProductList, '/product/list/')  # 产品列表
product.add_resource(ProductAdd, '/product/add/')  # 产品添加
product.add_resource(ProductDel, '/product/delete/')  # 产品删除
product.add_resource(ProductUpdate, '/product/update/')  # 产品更新
product.add_resource(CategorySeries, '/category/series/')  # 产品更新


_load_api = True
