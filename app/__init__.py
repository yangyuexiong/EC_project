# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午4:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint
from flask_restful import Api

from .api.index.index import IndexApi

from .crm.index.index import IndexCrmApi
from .crm.login.login import LoginCrmApi

"""front"""
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(IndexApi, '/', endpoint='api_index')

"""crm"""
crm_bp = Blueprint('cms', __name__)
crm_api = Api(crm_bp)
crm_api.add_resource(IndexCrmApi, '/', endpoint='crm_index')
crm_api.add_resource(LoginCrmApi, '/login', endpoint='login')
