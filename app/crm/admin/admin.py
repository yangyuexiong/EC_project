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

    def get(self, role_id):
        role_obj = Role.query.get(role_id)
        if role_obj:
            role = role_obj.to_json()
            return api_result(code=200, message='操作成功', data=role)
        else:
            ab_code_2(1000001)

    def post(self):
        data = request.get_json()
        role_name = data.get('role_name')
        remark = data.get('remark')
        if role_name:
            if Role.query.filter_by(name=role_name, is_deleted=0).first():
                ab_code_2(1000002)
            else:
                role = Role(name=role_name, creator=g.app_user.username, creator_id=g.app_user.id, remark=remark)
                db.session.add(role)
                db.session.commit()
                return api_result(code=201, message='操作成功', data=[])
        else:
            ab_code_2(1000001)

    def put(self):
        data = request.get_json()
        role_id = data.get('role_id')
        role_name = data.get('role_name')
        remark = data.get('remark')
        role = Role.query.get(role_id)
        if role:
            role.name = role_name
            role.remark = remark
            role.modifier = g.app_user.username
            role.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=203, message='操作成功', data=[])
        else:
            ab_code_2(1000001)

    def delete(self, role_id):
        role_obj = Role.query.get(role_id)
        if role_obj:
            role_obj.is_deleted = role_obj.id
            role_obj.modifier = g.app_user.username
            role_obj.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=204, message='操作成功', data=[])
        else:
            ab_code_2(1000001)


class PermissionCrmApi(Resource):
    """
    permission
    GET: 权限详情
    POST: 权限新增
    PUT: 权限编辑
    DELETE: 权限删除
    """

    def get(self, permission_id):
        permission_obj = Permission.query.get(permission_id)
        if permission_obj:
            permission = permission_obj.to_json()
            return api_result(code=200, message='操作成功', data=permission)
        else:
            ab_code_2(1000001)

    def post(self):
        data = request.get_json()
        permission_name = data.get('permission_name')
        resource_id = data.get('resource_id')
        resource_type = data.get('resource_type')
        remark = data.get('remark')
        if permission_name:
            if Permission.query.filter_by(name=permission_name, is_deleted=0).first():
                ab_code_2(1000002)
            else:
                permission = Permission(
                    name=permission_name,
                    resource_id=resource_id,
                    resource_type=resource_type,
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark=remark
                )
                db.session.add(permission)
                db.session.commit()
                return api_result(code=201, message='操作成功', data=[])
        else:
            ab_code_2(1000001)

    def put(self):
        data = request.get_json()
        permission_id = data.get('permission_id')
        permission_name = data.get('permission_name')
        resource_id = data.get('resource_id')
        resource_type = data.get('resource_type')
        remark = data.get('remark')
        permission = Permission.query.get(permission_id)
        if permission:
            permission.name = permission_name
            permission.resource_id = resource_id
            permission.resource_type = resource_type
            permission.remark = remark
            permission.modifier = g.app_user.username
            permission.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=203, message='操作成功', data=[])
        else:
            ab_code_2(1000001)

    def delete(self, permission_id):
        permission_obj = Permission.query.get(permission_id)
        if permission_obj:
            permission_obj.is_deleted = permission_obj.id
            permission_obj.modifier = g.app_user.username
            permission_obj.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=204, message='操作成功', data=[])
        else:
            ab_code_2(1000001)
