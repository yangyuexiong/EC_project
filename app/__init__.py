# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午4:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint
from flask_restful import Api

from .api.index.index import IndexApi

from .crm.search.search import SearchApi
from .crm.index.index import IndexCrmApi
from .crm.test.test import TestCrmApi
from .crm.admin.admin import AdminPageApi, AdminCrmApi, RolePageApi, RoleCrmApi, PermissionPageApi, PermissionCrmApi, \
    AdminRelRoleCrmApi, RoleRelPermissionCrmApi, ApiResourceCrmApi, ApiResourcePageCrmApi
from .crm.login.login import LoginCrmApi
from .crm.product.product import ProductCrmApi
from .crm.sku.sku import SkuApi, SkuPageApi
from .crm.order.order import OrderCrmApi

"""front"""
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(IndexApi, '/', endpoint='api_index')

"""crm"""
crm_bp = Blueprint('crm', __name__)
crm_api = Api(crm_bp)
crm_api.add_resource(IndexCrmApi, '/index', endpoint='crm_index')
crm_api.add_resource(TestCrmApi, '/test', endpoint='crm_test')
crm_api.add_resource(SearchApi, '/search', endpoint='crm_search')
crm_api.add_resource(LoginCrmApi, '/login', endpoint='crm_login')

crm_api.add_resource(AdminPageApi, '/admin/page', endpoint='crm_admin_page')
crm_api.add_resource(AdminCrmApi, '/admin', '/admin/<admin_id>', endpoint='crm_admin')
crm_api.add_resource(AdminRelRoleCrmApi, '/admin/rel', endpoint='crm_admin_rel')

crm_api.add_resource(RolePageApi, '/role/page', endpoint='crm_role_page')
crm_api.add_resource(RoleCrmApi, '/role', '/role/<role_id>', endpoint='crm_role')
crm_api.add_resource(RoleRelPermissionCrmApi, '/role/rel', '/role/rel/<role_id>', endpoint='crm_role_rel')

crm_api.add_resource(PermissionPageApi, '/permission/page', endpoint='crm_permission_page')
crm_api.add_resource(PermissionCrmApi, '/permission', '/permission/<permission_id>', endpoint='crm_permission')

crm_api.add_resource(ProductCrmApi, '/product', '/product/<product_id>', endpoint='crm_product')
crm_api.add_resource(SkuApi, '/sku', '/sku/<sku_id>', endpoint='crm_sku')
crm_api.add_resource(SkuPageApi, '/sku/page', endpoint='crm_sku_page')

crm_api.add_resource(ApiResourceCrmApi, '/api_resource', '/api_resource/<api_resource_id>', endpoint='crm_api_resource')
crm_api.add_resource(ApiResourcePageCrmApi, '/api_resource/page', endpoint='crm_api_resource_page')

crm_api.add_resource(OrderCrmApi, '/order', '/order/<order_id>', endpoint='crm_order')
