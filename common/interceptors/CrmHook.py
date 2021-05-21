# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 3:15 PM
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ApiHook.py
# @Software: PyCharm

from flask import request, g

from app import crm_bp
from app.models.admin.models import Admin
from common.libs.auth import check_user
from common.libs.tools import print_logs
from common.libs.customException import ab_code_2


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
        else:
            ab_code_2(666)

    else:
        g.app_user = None
