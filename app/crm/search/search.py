# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 下午1:36
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : search.py
# @Software: PyCharm


from flask_sqlalchemy.model import DefaultMeta

from app.all_reference import *
from common.libs.tools import general_paging_fuzzy_query as gq
from app.models.product.models import Product, AttributeKey, AttributeVal, Sku, ProductStock

classify_dict = {
    "1": "",  # 用户
    "2": "",  # 订单
    "3": Product,  # 商品
}


class SearchApi(Resource):
    """
    搜索
    """

    def post(self):
        data = request.get_json()
        classify = data.get('classify', None)
        q = data.get('q', '')
        like_params = data.get('like_params')
        where_dict = data.get('where_dict')
        page = data.get('page', 1)
        size = data.get('size', 20)
        model = classify_dict.get(str(classify))
        d = {
            "q": q,
            "model": model,
            "like_params": like_params,
            "where_dict": where_dict,
            "page": page,
            "size": size
        }
        if isinstance(like_params, list) and isinstance(where_dict, dict) and isinstance(model, DefaultMeta):
            result_list = gq(**d)
            return api_result(code=200, message='操作成功:{}'.format(classify), data=result_list)
        else:
            ab_code_2(900001)
