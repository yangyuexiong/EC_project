# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 下午1:36
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : search.py
# @Software: PyCharm

from app.all_reference import *


class SearchApi(Resource):
    """
    搜索
    """

    def post(self):
        """1"""
        data = request.get_json()
        d = {"name": "测试魔力套餐", "status": 0, "skuType": 1, "page": 1, "limit": 20, "search": {}}

        search = data.get('')
        q = "%" + search + "%"
        or_list = []
        for k, v in model.__dict__.items():
            # print(k, type(k), '======', v, type(v))
            try:
                if '__' in k:
                    pass
                else:
                    # print(v, type(v))
                    condition_obj = v.ilike(q if q is not None else '')  # 模糊条件
                    # print(type(x))
                    or_list.append(condition_obj)  # 整合
            except BaseException as e:
                pass
