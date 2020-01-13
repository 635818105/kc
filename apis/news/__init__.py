from flask import Blueprint
from flask_restful import Api
from apis.news.views import NewsList, NewsAdd, NewsDel, NewsUpdate

news_api_bp = Blueprint('news', __name__)
news = Api(news_api_bp)
# 产品
news.add_resource(NewsList, '/news/list/')  # 产品列表
news.add_resource(NewsAdd, '/news/add/')  # 产品添加
news.add_resource(NewsDel, '/news/delete/')  # 产品删除
news.add_resource(NewsUpdate, '/news/update/')  # 产品更新


_load_api = True