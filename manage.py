# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午4:32
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : manage.py
# @Software: PyCharm

import os
import random

from sqlalchemy import or_, and_
from flask_script import Manager, Server, Command
from flask_migrate import Migrate, MigrateCommand

from ApplicationExample import create_app
from ExtendRegister.db_register import db

from app.models.admin.models import Admin, Role, Permission, MidAdminAndRole, MidPermissionAndRole, ApiResource, \
    RouteResource
from app.models.product.models import ProductBrand, ProductCategory, Product, Sku, AttributeKey, AttributeVal, \
    ProductComment, ProductStock, ProductSales, ProductOperationLog

app = create_app()  # 实例
manager = Manager(app)  # 绑定
Migrate(app, db)
manager.add_command('db', MigrateCommand)  # 添加命令


# 自定义命令一：
class Hello(Command):
    """hello world"""

    def run(self):
        print('hello world')


class TableCreateFirst(Command):
    """首次映射并且创建表"""

    def run(self):
        try:
            os.system("python3 manage.py db init")
            os.system("python3 manage.py db migrate")
            os.system("python3 manage.py db upgrade")
            print('创建成功')
        except BaseException as e:
            print('创建失败:{}'.format(str(e)))


class TableCreate(Command):
    """增加表"""

    def run(self):
        try:
            os.system("python3 manage.py db migrate")
            os.system("python3 manage.py db upgrade")
            print('创建成功')
        except BaseException as e:
            print('创建失败:{}'.format(str(e)))


class CRMInit(Command):
    """CRM初始化"""

    def run(self):

        admin = {
            'username': 'admin',
            'password': '123456',
            'phone': '15013038819',
            'mail': 'yangyuexiong33@gmail.com',
            'code': '00001'
        }
        admin2 = {
            'username': 'admin2',
            'password': '123456',
            'phone': '15013038818',
            'mail': 'yangyuexiong33@gmail.com',
            'code': '00002'
        }
        admin3 = {
            'username': 'admin3',
            'password': '123456',
            'phone': '15013038817',
            'mail': 'yangyuexiong33@gmail.com',
            'code': '00003'
        }
        admin4 = {
            'username': 'admin4',
            'password': '123456',
            'phone': '15013038816',
            'mail': 'yangyuexiong33@gmail.com',
            'code': '00004'
        }

        admin_list = [admin, admin2, admin3, admin4]
        role_list = ['超级管理员', '管理员A', '管理员B', '管理员C', '管理员D']
        api_resource = [
            {
                'name': 'crm首页',
                'url': '/crm/index',
                'method': 'GET'
            },
            {
                'name': 'crm测试',
                'url': '/crm/test',
                'method': 'GET'
            },

            {
                'name': '用户列表',
                'url': '/crm/admin/page',
                'method': 'POST'
            },
            {
                'name': '用户详情',
                'url': '/crm/admin',
                'method': 'GET'
            },
            {
                'name': '用户新增',
                'url': '/crm/admin',
                'method': 'POST'
            },
            {
                'name': '用户编辑',
                'url': '/crm/admin',
                'method': 'PUT'
            },
            {
                'name': '用户(禁用/启用)',
                'url': '/crm/admin',
                'method': 'DELETE'
            },
            {
                'name': '用户配置角色',
                'url': '/crm/admin/rel',
                'method': 'POST'
            },

            {
                'name': '角色列表',
                'url': '/crm/role/page',
                'method': 'POST'
            },
            {
                'name': '角色详情',
                'url': '/crm/role',
                'method': 'GET'
            },
            {
                'name': '角色新增',
                'url': '/crm/role',
                'method': 'POST'
            },
            {
                'name': '角色编辑',
                'url': '/crm/role',
                'method': 'PUT'
            },
            {
                'name': '角色(禁用/启用)',
                'url': '/crm/role',
                'method': 'DELETE'
            },
            {
                'name': '角色配置权限',
                'url': '/crm/role/rel',
                'method': 'POST'
            },

            {
                'name': '权限列表',
                'url': '/crm/permission/page',
                'method': 'POST'
            },
            {
                'name': '权限详情',
                'url': '/crm/permission',
                'method': 'GET'
            },
            {
                'name': '权限新增',
                'url': '/crm/permission',
                'method': 'POST'
            },
            {
                'name': '权限编辑',
                'url': '/crm/permission',
                'method': 'PUT'
            },
            {
                'name': '权限(禁用/启用)',
                'url': '/crm/permission',
                'method': 'DELETE'
            },

            {
                'name': '接口列表',
                'url': '/crm/api_resource/page',
                'method': 'POST'
            },
            {
                'name': '接口详情',
                'url': '/crm/api_resource',
                'method': 'GET'
            },
            {
                'name': '接口新增',
                'url': '/crm/api_resource',
                'method': 'POST'
            },
            {
                'name': '接口编辑',
                'url': '/crm/api_resource',
                'method': 'PUT'
            },
            {
                'name': '接口(禁用/启用)',
                'url': '/crm/api_resource',
                'method': 'DELETE'
            },

        ]

        # 创建用户
        for ad in admin_list:
            print(ad)
            query_admin = Admin.query.filter(
                or_(Admin.username == ad.get('username'), Admin.phone == ad.get('phone'))).first()
            if query_admin:
                print('CRM用户: {} 已存在'.format(query_admin))
            else:
                new_admin = Admin(
                    username=ad.get('username'),
                    password=ad.get('password'),
                    phone=ad.get('phone'),
                    mail=ad.get('mail'),
                    code=ad.get('code'),
                    creator='shell',
                    creator_id='0',
                    remark='manage shell')
                db.session.add(new_admin)
                db.session.commit()
                print('CRM用户: {} 添加成功'.format(admin))

        # 创建角色
        for role in role_list:
            query_role = Role.query.filter_by(name=role).first()
            if query_role:
                print('CRM角色: {} 已存在'.format(query_role))
            else:
                new_role = Role(name=role, creator='shell', creator_id='0', remark='manage shell')
                db.session.add(new_role)
                db.session.commit()
                print('CRM角色: {} 添加成功'.format(role))

        # 创建权限
        for api in api_resource:
            name = api.get('name')
            url = api.get('url')
            method = api.get('method')
            query_api = ApiResource.query.filter(and_(ApiResource.url == url, ApiResource.method == method)).first()
            if query_api:
                print('CRM Api: {} 已存在'.format(query_api))
            else:
                api_resource = ApiResource(
                    name=name,
                    url=url,
                    method=api.get('method'),
                    creator='shell',
                    creator_id='0',
                    remark='manage shell'
                )
                db.session.add(api_resource)
                db.session.commit()
                print('CRM Api 创建完成:{}'.format(name))

                query_permission = Permission.query.filter_by(name=name).first()
                if query_permission:
                    print('CRM 权限: {} 已存在'.format(query_permission))
                else:
                    permission = Permission(
                        name=name,
                        resource_id=api_resource.id,
                        resource_type='SERVER_API',
                        creator='shell',
                        creator_id='0',
                        remark='manage shell'
                    )
                    db.session.add(permission)
                    db.session.commit()
                    print('CRM 权限 创建完成:{}'.format(name))

        # 为admin设置所有角色权限
        root_admin = Admin.query.filter_by(username='admin').first()
        super_role = Role.query.filter_by(name='超级管理员').first()
        all_role = Role.query.all()
        all_permission = Permission.query.all()

        # 配置权限
        for per in all_permission:
            query_mid_permission_role = MidPermissionAndRole.query.filter_by(
                role_id=super_role.id,
                permission_id=per.id).first()
            if query_mid_permission_role:
                print('角色:{} 已拥有权限:{}'.format(super_role.name, per.name))
            else:
                mid_permission_role = MidPermissionAndRole(
                    permission_id=per.id,
                    role_id=super_role.id,
                    creator='shell',
                    creator_id='0'
                )
                db.session.add(mid_permission_role)
                print('角色:{} 添加 权限:{} 完成'.format(super_role.name, per.name))
        db.session.commit()

        # 配置角色
        for role in all_role:
            query_mid_admin_role = MidAdminAndRole.query.filter_by(admin_id=root_admin.id, role_id=role.id).first()
            if query_mid_admin_role:
                print('用户:{} 已拥有角色:{}'.format(root_admin.username, role.name))
            else:
                mid_admin_role = MidAdminAndRole(
                    admin_id=root_admin.id,
                    role_id=role.id,
                    creator='shell',
                    creator_id='0'
                )
                db.session.add(mid_admin_role)
                print('用户:{} 添加 角色:{} 完成'.format(root_admin.username, role.name))
        db.session.commit()


class SkuInit(Command):
    """Sku Demo"""

    def run(self):
        l = [
            {
                "口味": "鲜奶",
                "温度": "少冰",
                "甜度": "少糖",

            },
            {
                "口味": "轻脂",
                "温度": "去冰",
                "甜度": "多糖",
            }
        ]
        for i in l:
            print(i)
            spec = i
            new_sku1 = Sku(product_id=1, spec=spec)
            new_sku2 = Sku(product_id=2, spec=spec)
            new_sku3 = Sku(product_id=3, spec=spec)
            db.session.add_all([new_sku1, new_sku2, new_sku3])
        db.session.commit()


# 添加命令
manager.add_command('hello', Hello())
manager.add_command('orm', TableCreateFirst())
manager.add_command('table', TableCreate())
manager.add_command('crm', CRMInit())


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_cms_user(username, password):
    """创建后台管理用户"""
    user = Admin(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('CRM用户添加成功')


# 自定义命令二：
# web server
manager.add_command("runserver",
                    Server(
                        host='0.0.0.0',
                        port=7777,
                        use_debugger=True,
                        use_reloader=True
                    ))


def main():
    manager.run()


if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()

    '''
    数据库
    在pipenv环境中在每个命令前加上 pipenv run
    如:pipenv run python3 manage.py 
    '''
    # 初始化迁移环境:python3 manage.py db init
    # 迁移数据库:python3 manage.py db migrate
    # 映射数据库:python3 manage.py db upgrade
    # 回滚:
    #   ps:先备份数据
    #       python3 manage.py db history
    #       python3 manage.py db downgrade id

    '''库表初始化'''
    # python3 manage.py orm

    '''CRM初始化'''
    # python3 manage.py crm
