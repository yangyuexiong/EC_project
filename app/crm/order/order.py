# -*- coding: utf-8 -*-
# @Time    : 2021/5/28 下午5:17
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : order.py
# @Software: PyCharm

from app.all_reference import *
from app.models.order.models import Order


class OrderCrmApi(Resource):
    """
    订单
    GET: 订单详情
    POST: 订单分页查询
    PUT: 订单状态更改
    DELETE: 订单删除
    """

    def get(self, order_id):
        return api_result(code=200, message='操作成功')

    def post(self):
        return api_result(code=200, message='操作成功')

    def put(self):
        return api_result(code=203, message='操作成功')

    def delete(self):
        return api_result(code=204, message='操作成功')
