# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午5:22
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : index.py
# @Software: PyCharm

from app.all_reference import *


class IndexApi(Resource):
    """
    index
    """

    def get(self):
        return api_result(code=200, message='api index')
