# -*- coding: utf-8 -*-
# @Time    : 2021/5/21 下午2:27
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : admin.py
# @Software: PyCharm

from app.all_reference import *
from app.models.admin.models import Admin, Role, Permission, MidAdminAndRole, MidPermissionAndRole, ApiResource, \
    RouteResource


# Todo 用户,角色,权限操作的装饰器
# Todo PUT编辑调用 query_admin_permission_info(admin_id)

def query_admin_permission_info(admin_id):
    """
    获取用户角色权限
    :param admin_id:
    :return:
    """
    query_admin = """
        SELECT 
        id,username,phone,mail,code,creator,modifier,create_time,update_time,is_deleted,status,remark 
        FROM ec_crm_admin 
        WHERE id={};""".format(admin_id)
    admin_res = project_db.select(query_admin, only=True)
    print(query_admin)
    # print(admin_res)

    if admin_res:
        query_role = """
        SELECT 
        id,name,creator,modifier,create_time,update_time,is_deleted,status,remark 
        FROM ec_crm_role 
        WHERE id in (SELECT role_id FROM ec_crm_mid_admin_role WHERE admin_id={});""".format(admin_id)
        role_res = project_db.select(query_role)
        print(query_role)
        # print(role_res)

        role_id_list = [r_id.get('id') for r_id in role_res]
        # print(tuple(role_id_list))

        query_permission = """
        SELECT 
        P.id,
        P.name,
        P.resource_id,
        P.resource_type,
        API.name,
        API.url,
        API.method,
        P.is_deleted,
        P.creator,
        P.modifier,
        P.create_time,
        P.update_time,
        P.remark,
        API.remark
        FROM ec_crm_permission P LEFT JOIN ec_crm_api_resource API ON P.resource_id=API.id  
        WHERE P.id in (SELECT permission_id FROM ec_crm_mid_permission_role WHERE role_id in {});
        """.format(tuple(role_id_list))
        permission_res = project_db.select(query_permission)
        print(query_permission)
        # print(permission_res)
        url_list = []
        route_list = []
        other_list = []
        for p in permission_res:
            url = p.get('url')
            resource_type = p.get('resource_type')
            if resource_type == 'SERVER_API':
                url_list.append(url)
            elif resource_type == 'WEB_ROUTE':
                route_list.append(url)
            else:
                other_list.append(url)

        admin_res['role_list'] = role_res
        admin_res['role_id_list'] = role_id_list
        admin_res['permission_list'] = permission_res
        admin_res['url_list'] = url_list
        admin_res['route_list'] = route_list
        admin_res['other_list'] = other_list

        redis_key = 'auth:{}'.format(admin_id)
        R.set(redis_key, json.dumps(admin_res))
        return admin_res
    else:
        return admin_res


"""admin"""


class AdminPageApi(Resource):
    """
    admin page api
    POST: admin分页模糊查询
    """

    def post(self):
        data = request.get_json()
        admin_id = data.get('admin_id')
        username = data.get('username')
        phone = data.get('phone')
        is_deleted = data.get('is_deleted')
        page, size = page_size(**data)

        sql = """
        SELECT * 
        FROM ec_crm_admin  
        WHERE 
        id LIKE"%%" 
        and username LIKE"%c%" 
        and phone LIKE"%150%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        like_list = [
            Admin.id.ilike("%{}%".format(admin_id if admin_id else '')),
            Admin.username.ilike("%{}%".format(username if username else '')),
            Admin.phone.ilike("%{}%".format(phone if phone else ''))
        ]

        where_list = []
        where_list.append(Admin.is_deleted != 0) if is_deleted and is_deleted != 0 else where_list.append(
            Admin.is_deleted == 0)

        result = Admin.query.filter(
            and_(*like_list),
            *where_list
        ).order_by(
            Admin.create_time.desc()
        ).paginate(
            page=int(page),
            per_page=int(size),
            error_out=False
        )
        result_list = []
        total = result.total
        for res in result.items:
            admin_json = res.to_json(*['_password'])
            result_list.append(admin_json)

        result_data = {
            'records': result_list,
            'now_page': page,
            'total': total
        }
        return api_result(code=200, message='操作成功', data=result_data)


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
            query_admin_role_permission(admin_id)
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
        data = request.get_json()
        admin_id = data.get('admin_id')
        is_deleted = data.get('is_deleted')
        admin = Admin.query.get(admin_id)
        if admin:
            admin.is_deleted = is_deleted if is_deleted in [0, '0'] else admin.id
            admin.modifier = g.app_user.username
            admin.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=204, message='操作成功')
        else:
            ab_code_2(1000001)


"""role"""


class RolePageApi(Resource):
    """
    role page api
    POST: role分页模糊查询
    """

    def post(self):
        data = request.get_json()
        role_id = data.get('role_id')
        name = data.get('name')
        page, size = page_size(**data)

        sql = """
        SELECT *
        FROM ec_crm_role
        WHERE
        id LIKE"%%"
        and name LIKE"%超级%"
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        like_list = [
            Role.id.ilike("%{}%".format(role_id if role_id else '')),
            Role.name.ilike("%{}%".format(name if name else ''))
        ]
        where_list = [
            Role.is_deleted == 0
        ]
        result = Role.query.filter(
            and_(*like_list),
            *where_list
        ).order_by(
            Role.create_time.desc()
        ).paginate(
            page=int(page),
            per_page=int(size),
            error_out=False
        )
        result_list = []
        total = result.total
        for res in result.items:
            role_json = res.to_json()
            result_list.append(role_json)

        result_data = {
            'records': result_list,
            'now_page': page,
            'total': total
        }
        return api_result(code=200, message='操作成功', data=result_data)


class RoleCrmApi(Resource):
    """
    role
    GET: 角色详情
    POST: 角色新增
    PUT: 角色编辑
    DELETE: 角色(启用/禁用)
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

    def delete(self):
        data = request.get_json()
        role_id = data.get('role_id')
        is_deleted = data.get('is_deleted')
        role = Role.query.get(role_id)
        if role:
            role.is_deleted = is_deleted if is_deleted in [0, '0'] else role.id
            role.modifier = g.app_user.username
            role.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=204, message='操作成功')
        else:
            ab_code_2(1000001)


"""permission"""


class PermissionPageApi(Resource):
    """
    permission page api
    POST: permission分页模糊查询
    """

    def post(self):
        data = request.get_json()
        permission_id = data.get('permission_id')
        permission_name = data.get('permission_name')
        api_name = data.get('api_name')
        url = data.get('url')
        page, size = page_size(**data)

        sql = """
        SELECT
        P.id,
        P.name,
        P.resource_id,
        P.resource_type,
        API.id,
        API.name,
        API.url,
        API.method 
        FROM ec_crm_permission P LEFT JOIN ec_crm_api_resource API ON P.resource_id=API.id 
        WHERE (
        P.id LIKE"%%" 
        and P.name LIKE"%B%" 
        and API.id LIKE"%%" 
        and API.name LIKE"%%" 
        and API.url LIKE"%%"
        )
        and P.is_deleted=0 and API.is_deleted=0
        ORDER BY P.create_timestamp LIMIT 0,20;
        """

        like_list = [
            Permission.id.ilike("%{}%".format(permission_id if permission_id else '')),
            Permission.name.ilike("%{}%".format(permission_name if permission_name else '')),
            ApiResource.name.ilike("%{}%".format(api_name if api_name else '')),
            ApiResource.url.ilike("%{}%".format(url if url else ''))
        ]
        where_list = [
            Permission.is_deleted == 0
        ]

        result = Permission.query.join(
            ApiResource,
            Permission.resource_id == ApiResource.id
        ).filter(
            and_(*like_list),
            *where_list
        ).with_entities(
            Permission, ApiResource
        ).order_by(
            Permission.create_time.desc()
        ).paginate(
            page=int(page),
            per_page=int(size),
            error_out=False
        )

        result_list = []
        total = result.total
        for res in result.items:
            permission_json = res[0].to_json()
            api_resource_json = res[1].to_json()
            permission_json['api_resource_json'] = api_resource_json
            result_list.append(permission_json)

        result_data = {
            'records': result_list,
            'now_page': page,
            'total': total
        }
        return api_result(code=200, message='操作成功', data=result_data)


class PermissionCrmApi(Resource):
    """
    permission
    GET: 权限详情
    POST: 权限新增
    PUT: 权限编辑
    DELETE: 权限(启用/禁用)
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

    def delete(self):
        data = request.get_json()
        permission_id = data.get('permission_id')
        is_deleted = data.get('is_deleted')
        permission = Permission.query.get(permission_id)
        if permission:
            permission.is_deleted = is_deleted if is_deleted in [0, '0'] else permission.id
            permission.modifier = g.app_user.username
            permission.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=204, message='操作成功')
        else:
            ab_code_2(1000001)


"""rel"""


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
                    query_admin_permission_info(admin_id=admin_id)
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
    GET: 查询角色下所有权限
    POST: 角色(添加/删除)权限
    """

    def get(self, role_id):
        role_obj = Role.query.get(role_id)
        if role_obj:
            role = role_obj.to_json()
            mid_list = [p.permission_id for p in MidPermissionAndRole.query.filter_by(role_id=role_id).all()]
            if mid_list:
                sql = """
                SELECT
                P.id,
                P.name,
                P.creator_id,
                P.creator,
                P.create_time,
                API.id,
                API.name,
                API.url,
                API.method,
                API.creator_id,
                API.creator,
                API.create_time
                FROM ec_crm_permission P LEFT JOIN ec_crm_api_resource API ON P.resource_id=API.id 
                WHERE 
                (P.is_deleted=0 and API.is_deleted=0)
                ORDER BY P.create_timestamp LIMIT 0,20;
                """
                where_list = [
                    Permission.is_deleted == 0,
                    ApiResource.is_deleted == 0
                ]
                result = Permission.query.join(
                    ApiResource,
                    Permission.resource_id == ApiResource.id
                ).filter(
                    *where_list
                ).with_entities(
                    Permission, ApiResource
                ).order_by(
                    Permission.create_time.desc()
                ).all()

                result_list = []
                for res in result:
                    permission_json = res[0].to_json()
                    api_resource_json = res[1].to_json()
                    permission_json['api_resource_json'] = api_resource_json
                    result_list.append(permission_json)

                role['permission_list'] = result_list
                return api_result(code=200, message='操作成功', data=role)
            else:
                role['permission_list'] = []
                return api_result(code=200, message='操作成功', data=role)
        else:
            ab_code_2(1000001)

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

                    admin_id_list = [m.admin_id for m in MidAdminAndRole.query.filter_by(role_id=role_id).all()]
                    [query_admin_permission_info(admin_id=a_id) for a_id in admin_id_list]

                    return api_result(code=201, message='操作成功', data=admin_id_list)
                else:
                    ab_code_2(1000001)
            else:
                ab_code_2(1000001)
        else:
            ab_code_2(1000001)


"""resource"""


class ApiResourceCrmApi(Resource):
    """
    权限关联接口
    GET: 接口详情
    POST: 接口新增
    PUT: 接口编辑
    DELETE: 接口(启用/禁用)
    """

    def get(self, api_resource_id):
        api_res_obj = ApiResource.query.get(api_resource_id)
        if api_res_obj:
            api_res = api_res_obj.to_json()
            return api_result(code=200, message='操作成功', data=api_res)
        else:
            ab_code_2(1000001)

    def post(self):
        data = request.get_json()
        name = data.get('name')
        url = data.get('url')
        method = data.get('method')
        remark = data.get('remark')
        if name and url:
            api_res = ApiResource.query.filter(or_(ApiResource.name == name, ApiResource.url == url)).first()
            if name and url and not api_res:
                new_api_res = ApiResource(name=name, url=url, method=method, remark=remark)
                db.session.add(new_api_res)
                db.session.commit()
                return api_result(code=201, message='操作成功')
            else:
                return api_result(code=200, message='接口或名称已经存在')
        else:
            ab_code_2(1000001)

    def put(self):
        data = request.get_json()
        api_resource_id = data.get('api_resource_id')
        name = data.get('name')
        url = data.get('url')
        method = data.get('method')
        remark = data.get('remark')
        if name and url:
            api_res = ApiResource.query.get(api_resource_id)
            api_query = ApiResource.query.filter(or_(ApiResource.name == name, ApiResource.url == url)).first()
            if api_res and not api_query:
                api_res.name = name
                api_res.url = url
                api_res.method = method
                api_res.remark = remark
                api_res.modifier = g.app_user.username
                api_res.modifier_id = g.app_user.id
                db.session.commit()
                return api_result(code=203, message='操作成功')
            else:
                return api_result(code=200, message='接口或名称已经存在')
        else:
            ab_code_2(1000001)

    def delete(self):
        data = request.get_json()
        api_resource_id = data.get('api_resource_id')
        is_deleted = data.get('is_deleted')
        api_res = ApiResource.query.get(api_resource_id)
        if api_res:
            api_res.is_deleted = is_deleted if is_deleted in [0, '0'] else api_res.id
            api_res.modifier = g.app_user.username
            api_res.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=204, message='操作成功')
        else:
            ab_code_2(1000001)


class ApiResourcePageCrmApi(Resource):
    """
    api resource page
    POST: api resource 分页模糊查询
    """

    def post(self):
        data = request.get_json()
        api_resource_id = data.get('api_resource_id')
        name = data.get('name')
        url = data.get('url')
        page, size = page_size(**data)

        sql = """
        SELECT * 
        FROM ec_crm_api_resource 
        WHERE (id LIKE"%%" and name LIKE"%ok%" and url LIKE"%%") 
        and is_deleted=0 
        ORDER BY create_timestamp LIMIT 0,20;
        """

        like_list = [
            ApiResource.id.ilike("%{}%".format(api_resource_id if api_resource_id else '')),
            ApiResource.name.ilike("%{}%".format(name if name else '')),
            ApiResource.url.ilike("%{}%".format(url if url else ''))
        ]
        where_list = [
            ApiResource.is_deleted == 0
        ]

        result = ApiResource.query.filter(
            and_(*like_list),
            *where_list
        ).order_by(
            ApiResource.create_time.desc()
        ).paginate(
            page=int(page),
            per_page=int(size),
            error_out=False
        )
        result_list = []
        total = result.total
        for res in result.items:
            result_list.append(res.to_json())
        result_data = {
            'records': result_list,
            'now_page': page,
            'total': total
        }
        return api_result(code=200, message='操作成功', data=result_data)


class RouteResourceCrmApi(Resource):
    """
    权限页面路由
    """
