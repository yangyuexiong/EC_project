# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 3:15 PM
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ApiHook.py
# @Software: PyCharm

import re
import json

from flask import request, g

from app import crm_bp
from app.models.admin.models import Admin
from common.libs.auth import check_user, R
from common.libs.tools import print_logs
from common.libs.customException import ab_code_2
from common.libs.utils import AdminRefreshCache


@crm_bp.before_request
def before_request_cms():
    print('cms_before_request')
    print_logs()

    white_list = ['/crm/login']
    if request.path in white_list:
        print('white_list:', white_list)
        return

    if '/crm' in request.path:
        is_token = request.headers.get('Token', None)  # 是否存在token
        print('头部是否存在key:token->', is_token)
        if is_token:
            token = request.headers.get('token', '')  # 提取token
            # print(token)
            # 通过 token 查找 user
            # 将 user 存放在全局 g 对象中
            check_user(token=token, model=Admin)

            admin_id = g.app_user.id
            admin_auth_result = R.get('auth:{}'.format(admin_id))
            if admin_auth_result:
                print('Redis缓存情况')
                admin_role_permission = json.loads(admin_auth_result)
                url_list = admin_role_permission.get('url_list')
                url_is_var_list = admin_role_permission.get('url_is_var_list')
                url_tuple_list = [tuple(t) for t in admin_role_permission.get('url_tuple_list')]
                url_is_var_tuple_list = [tuple(t) for t in admin_role_permission.get('url_is_var_tuple_list')]
                print(url_list)
                print(url_is_var_list)
                print('==========')
                print(url_tuple_list)
                print(url_is_var_tuple_list)

            else:
                print('无缓存情况')
                admin = AdminRefreshCache.query_admin_permission_info(admin_id=admin_id)
                url_list = admin.get('url_list', [])
                url_is_var_list = admin.get('url_is_var_list', [])
                url_tuple_list = admin.get('url_tuple_list', [])
                url_is_var_tuple_list = admin.get('url_is_var_tuple_list', [])
                print(url_list)
                print(url_is_var_list)
                print('==========')
                print(url_tuple_list)
                print(url_is_var_tuple_list)

            req_tuple = (request.method, request.path)
            print(req_tuple)

            pattern = '|'.join(['^{}/\w+'.format(is_var_url[1]) for is_var_url in url_is_var_tuple_list])
            print(pattern)
            re_result = re.search(pattern, request.path)
            print(re_result)
            print(bool(re_result))

            # Todo 多级url中包含相同uri无法识别

            if req_tuple in url_tuple_list:
                return
            elif bool(re_result):
                return
            else:
                ab_code_2(1000000)
        else:
            ab_code_2(666)

    else:
        g.app_user = None
