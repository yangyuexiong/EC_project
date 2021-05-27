# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午5:39
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : index.py
# @Software: PyCharm

from app.all_reference import *


class IndexCrmApi(Resource):
    """
    index
    """

    def get(self):
        print(request.args.get('test'))
        return api_result(code=200, message='crm index')
