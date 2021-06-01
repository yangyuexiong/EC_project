# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 10:47 AM
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : bp_register.py
# @Software: PyCharm


from app import api_bp, crm_bp

from flask import Blueprint

other_module = Blueprint('other_module', __name__)


@other_module.route('/', methods=["GET", "POST"])
async def module_01():
    return '其他业务模块001'


def register_bp(app):
    """蓝图注册"""

    """API蓝图注册"""
    app.register_blueprint(api_bp, url_prefix="/api")

    """CMS蓝图注册"""
    app.register_blueprint(crm_bp, url_prefix="/crm")

    """其他独立蓝图注册"""
    app.register_blueprint(other_module, url_prefix="/m1")
