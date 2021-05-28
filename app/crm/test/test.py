# -*- coding: utf-8 -*-
# @Time    : 2021/5/21 下午2:21
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test.py
# @Software: PyCharm


from app.all_reference import *


class TestCrmApi(Resource):
    """
    test
    """

    def get(self):
        return api_result(code=200, message='crm test')
