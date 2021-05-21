# -*- coding: utf-8 -*-
# @Time    : 2021/5/21 下午2:27
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : admin.py
# @Software: PyCharm

from app.all_reference import *
from app.models.admin.models import Admin, Role, Permission, MidAdminAndRole, MidPermissionAndRole, ApiResource, \
    RouteResource


class AdminCrmApi(Resource):
    """
    admin
    """

    def get(self):
        return api_result(code=200, message='admin index')


class RoleCrmApi(Resource):
    """
    role
    GET: 角色详情
    POST: 角色新增
    PUT: 角色编辑
    DELETE: 角色删除
    """

    def post(self):
        data = request.get_json()
        role_name = data.get('role_name')
        if role_name:
            if Role.query.filter_by(name=role_name, is_deleted=0).first():
                ab_code_2(1000002)
            else:
                role = Role(name=role_name)
                db.session.add(role)
                db.session.commit()
                return api_result(code=201, message='操作成功', data=[])
        else:
            ab_code_2(1000001)

    def delete(self, role_id):
        role_obj = Role.query.get(role_id)
        if role_obj:
            role_obj.is_deleted = role_obj.id
            db.session.commit()
            return api_result(code=204, message='操作成功', data=[])
        else:
            ab_code_2(1000001)


class PermissionCrmApi(Resource):
    """
    permission
    """
