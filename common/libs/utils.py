# -*- coding: utf-8 -*-
# @Time    : 2021/5/26 上午11:08
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : utils.py
# @Software: PyCharm

import json
import time

from common.libs.auth import R
from common.libs.tools import project_db, logger
from app.models.admin.models import Admin, Role, Permission, MidAdminAndRole, MidPermissionAndRole, ApiResource


def gen_order_number():
    """生成订单号"""
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')
    return order_no


def page_size(page=None, size=None, **kwargs):
    """

    :param page: -> int
    :param size: -> int
    :param kwargs: {"page":1,"size":20}
    :return:
    """
    page = page if page and isinstance(page, int) else int(kwargs.get('page', 0))
    size = size if size and isinstance(size, int) else int(kwargs.get('size', 20))
    page = (page - 1) * size if page != 0 else 0
    return page, size


class AdminRefreshCache:
    """获取用户角色权限并Redis缓存"""

    admin_id_list = []

    @classmethod
    def query_admin_permission_info(cls, admin_id):
        """
        获取用户角色权限并Redis缓存
        :param admin_id:
        :return:
        """
        query_admin = """
            SELECT 
            id,username,phone,mail,code,creator,modifier,create_time,update_time,is_deleted,status,remark 
            FROM ec_crm_admin 
            WHERE is_deleted=0 and id={};""".format(admin_id)
        admin_res = project_db.select(query_admin, only=True)
        logger.success(query_admin)
        # print(admin_res)

        if admin_res:
            query_role = """
            SELECT 
            id,name,creator,modifier,create_time,update_time,is_deleted,status,remark 
            FROM ec_crm_role 
            WHERE is_deleted=0 and id in (SELECT role_id FROM ec_crm_mid_admin_role WHERE admin_id={});""".format(
                admin_id)
            role_res = project_db.select(query_role)
            logger.success(query_role)
            # print(role_res)
            if role_res:
                role_id_list = [r_id.get('id') for r_id in role_res]
                # print(tuple(role_id_list))

                to_role_id_list = str(tuple(role_id_list)).replace(',', '') if len(role_id_list) == 1 else tuple(
                    role_id_list)
                # print(to_role_id_list)

                query_permission = """
                SELECT 
                P.id,
                P.name,
                P.resource_id,
                P.resource_type,
                API.name,
                API.url,
                API.method,
                API.is_url_var,
                P.is_deleted,
                P.creator,
                P.modifier,
                P.create_time,
                P.update_time,
                P.remark,
                API.remark
                FROM ec_crm_permission P LEFT JOIN ec_crm_api_resource API ON P.resource_id=API.id  
                WHERE P.is_deleted=0 and P.id in (SELECT permission_id FROM ec_crm_mid_permission_role WHERE role_id in {});
                """.format(to_role_id_list)
                permission_res = project_db.select(query_permission)
                logger.success(query_permission)
                # print(permission_res)

                if permission_res:
                    url_list = []
                    url_is_var_list = []
                    url_tuple_list = []
                    url_is_var_tuple_list = []
                    route_list = []
                    other_list = []
                    for p in permission_res:
                        method = p.get('method')
                        url = p.get('url')
                        is_url_var = p.get('is_url_var')
                        resource_type = p.get('resource_type')
                        if resource_type == 'SERVER_API':
                            t = (method, url)
                            if bool(is_url_var):
                                url_is_var_list.append(url)
                                url_is_var_tuple_list.append(t)
                            else:
                                url_list.append(url)
                                url_tuple_list.append(t)
                        elif resource_type == 'WEB_ROUTE':
                            route_list.append(url)
                        else:
                            other_list.append(url)

                    admin_res['role_list'] = role_res
                    admin_res['role_id_list'] = role_id_list
                    admin_res['permission_list'] = permission_res
                    admin_res['url_list'] = url_list
                    admin_res['url_is_var_list'] = url_is_var_list
                    admin_res['url_tuple_list'] = url_tuple_list
                    admin_res['url_is_var_tuple_list'] = url_is_var_tuple_list
                    admin_res['route_list'] = route_list
                    admin_res['other_list'] = other_list

                    redis_key = 'auth:{}'.format(admin_id)
                    R.set(redis_key, json.dumps(admin_res))
                    return admin_res
                else:
                    return admin_res
            else:
                return admin_res
        else:
            return admin_res

    @classmethod
    def query_admin_id_from_role(cls, role_id):
        """
        查询包含角色的所有用户
        :param role_id:
        :return:
        """
        cls.admin_id_list = [m.admin_id for m in MidAdminAndRole.query.filter_by(role_id=role_id).all()]

    @classmethod
    def query_admin_id_from_permission(cls, permission_id):
        """
        查询包含权限的所有用户
        :param permission_id:
        :return:
        """
        role_id_list = [m.role_id for m in MidPermissionAndRole.query.filter_by(permission_id=permission_id).all()]
        cls.admin_id_list = [
            m.admin_id for m in MidAdminAndRole.query.filter(MidAdminAndRole.role_id.in_(role_id_list)).all()
        ]

    @classmethod
    def query_admin_id_from_api_resource(cls, api_resource_id):
        """
        查询包含api_resource的所有用户
        :param api_resource_id:
        :return:
        """
        sql = """SELECT P.id 
        FROM ec_crm_permission P LEFT JOIN ec_crm_api_resource API ON P.resource_id=API.id  
        WHERE API.id={};""".format(api_resource_id)
        result = project_db.select(sql, only=True)
        permission_id = result.get('id')
        role_id_list = [role.id for role in MidPermissionAndRole.query.filter_by(permission_id=permission_id).all()]
        cls.admin_id_list = [
            m.admin_id for m in MidAdminAndRole.query.filter(MidAdminAndRole.role_id.in_(role_id_list)).all()
        ]

    @classmethod
    def refresh(cls, *args):
        """
        刷新缓存
        :param args:
        :return:
        """
        logger.success('===refresh===')

        if args:
            [cls.query_admin_permission_info(admin_id=admin_id) for admin_id in args]
        else:
            [cls.query_admin_permission_info(admin_id=admin_id) for admin_id in cls.admin_id_list]
