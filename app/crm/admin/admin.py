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
    GET: 后台用户详情
    POST: 后台用户创建
    PUT: 后台用户编辑
    DELETE: 后台用户(启用/禁用)
    """

    def get(self, admin_id):
        admin_boj = Admin.query.get(admin_id)
        if admin_boj:
            admin = admin_boj.to_json(*['_password'])
            return api_result(code=200, message='操作成功', data=admin)
        else:
            ab_code_2(1000001)

    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        mail = data.get('mail')
        remark = data.get('remark')

        if username and password:
            query_admin = Admin.query.filter(
                or_(Admin.username == username, Admin.phone == phone, Admin.mail == mail)).all()
            if query_admin:
                return api_result(code=200, message='用户已存在', data=[])
            else:
                code = str(Admin.query.count() + 1)
                admin = Admin(
                    username=username,
                    password=password,
                    phone=phone,
                    mail=mail,
                    code=code.zfill(5),
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark=remark
                )
                db.session.add(admin)
                db.session.commit()
                return api_result(code=201, message='操作成功', data=[])
        else:
            ab_code_2(1000001)

    def delete(self):
        return


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


class AdminRelRoleCrmApi(Resource):
    """
    admin rel role
    POST: 用户(添加/删除)角色
    """

    def post(self):
        data = request.get_json()
        admin_id = data.get('admin_id')
        role_list = data.get('role_list', [])
        keep_list = []  # 保留 -> is_deleted = 0
        del_list = []  # 逻辑删除 -> is_deleted = 非 0
        new_list = []  # 新增

        if isinstance(role_list, list):
            role_result = Role.query.filter(Role.id.in_(role_list)).all()
            if len(role_result) == len(role_list):
                admin = Admin.query.get(admin_id)
                if admin:
                    roles = [i.role_id for i in MidAdminAndRole.query.filter_by(admin_id=admin_id).all()]
                    for current_role in roles:
                        if current_role in role_list:
                            keep_list.append(current_role)
                        else:
                            del_list.append(current_role)

                    a = set(keep_list)
                    b = set(role_list)
                    a.update(b)
                    new_list = list(b - set(keep_list))
                    # print(keep_list)
                    # print(del_list)
                    # print(new_list)

                    if keep_list:
                        mid_a_r_list = MidAdminAndRole.query.filter(
                            MidAdminAndRole.admin_id == admin_id,
                            MidAdminAndRole.role_id.in_(keep_list)
                        ).all()
                        for mid in mid_a_r_list:
                            mid.is_deleted = 0
                            mid.modifier = g.app_user.username
                            mid.modifier_id = g.app_user.id

                    if del_list:
                        mid_a_r_list = MidAdminAndRole.query.filter(
                            MidAdminAndRole.admin_id == admin_id,
                            MidAdminAndRole.role_id.in_(del_list)
                        ).all()

                        for mid in mid_a_r_list:
                            mid.is_deleted = mid.id
                            mid.modifier = g.app_user.username
                            mid.modifier_id = g.app_user.id

                    if new_list:
                        for role_id in new_list:
                            mid_a_r = MidAdminAndRole(
                                admin_id=admin_id,
                                role_id=role_id,
                                creator=g.app_user.username,
                                creator_id=g.app_user.id
                            )
                            db.session.add(mid_a_r)
                    db.session.commit()
                    return api_result(code=201, message='操作成功', data=[])
                else:
                    ab_code_2(1000001)
            else:
                ab_code_2(1000001)
        else:
            ab_code_2(1000001)


class RoleRelPermissionCrmApi(Resource):
    """
    role rel permission
    POST: 角色(添加/删除)权限
    """

    def post(self):
        data = request.get_json()
        role_id = data.get('role_id')
        permission_list = data.get('permission_list', [])
        keep_list = []  # 保留 -> is_deleted = 0
        del_list = []  # 逻辑删除 -> is_deleted = 非 0
        new_list = []  # 新增

        if isinstance(permission_list, list):
            permission_result = Permission.query.filter(Permission.id.in_(permission_list)).all()
            if len(permission_result) == len(permission_list):
                role = Role.query.get(role_id)
                if role:
                    permissions = [i.permission_id for i in MidPermissionAndRole.query.filter_by(role_id=role_id).all()]
                    for current_p in permissions:
                        if current_p in permission_list:
                            keep_list.append(current_p)
                        else:
                            del_list.append(current_p)

                    a = set(keep_list)
                    b = set(permission_list)
                    a.update(b)
                    new_list = list(b - set(keep_list))

                    # print(keep_list)
                    # print(del_list)
                    # print(new_list)

                    if keep_list:
                        mid_p_r_list = MidPermissionAndRole.query.filter(
                            MidPermissionAndRole.role_id == role_id,
                            MidPermissionAndRole.permission_id.in_(keep_list)
                        ).all()
                        for mid in mid_p_r_list:
                            mid.is_deleted = 0
                            mid.modifier = g.app_user.username
                            mid.modifier_id = g.app_user.id

                    if del_list:
                        mid_p_r_list = MidPermissionAndRole.query.filter(
                            MidPermissionAndRole.role_id == role_id,
                            MidPermissionAndRole.permission_id.in_(del_list)
                        ).all()

                        for mid in mid_p_r_list:
                            mid.is_deleted = mid.id
                            mid.modifier = g.app_user.username
                            mid.modifier_id = g.app_user.id

                    if new_list:
                        for p in new_list:
                            mid_r_p = MidPermissionAndRole(
                                permission_id=p,
                                role_id=role.id,
                                creator=g.app_user.username,
                                creator_id=g.app_user.id
                            )
                            db.session.add(mid_r_p)
                    db.session.commit()
                    return api_result(code=201, message='操作成功', data=[])
                else:
                    ab_code_2(1000001)
            else:
                ab_code_2(1000001)
        else:
            ab_code_2(1000001)
