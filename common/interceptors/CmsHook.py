# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 3:15 PM
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ApiHook.py
# @Software: PyCharm

from flask import request

from app import crm_bp
from common.libs.tools import print_logs


@crm_bp.before_request
def before_request_cms():
    print('cms_before_request')
    print_logs()
    if '/cms' in request.path:
        print('cms')
        return