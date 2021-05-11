# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午4:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : all_reference.py
# @Software: PyCharm

import os
import threading

from flask_restful import Resource
from flask.views import MethodView
from flask import abort, render_template

from common.libs.api_result import api_result
from common.libs.customException import ab_code, ab_code_2
from ExtendRegister.db_register import db