# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午4:32
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : manage.py
# @Software: PyCharm

import os
import random

from sqlalchemy import or_
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
            }
        ]
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

        for role in role_list:
            query_role = Role.query.filter_by(name=role).first()
            if query_role:
                print('CRM角色: {} 已存在'.format(query_role))
            else:
                new_role = Role(name=role, creator='shell', creator_id='0', remark='manage shell')
                db.session.add(new_role)
                db.session.commit()
                print('CRM角色: {} 添加成功'.format(role))

        for api in api_resource:
            name = api.get('name')
            url = api.get('url')
            query_api = ApiResource.query.filter(or_(ApiResource.name == name, ApiResource.url == url)).first()
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


class CommodityInit(Command):
    """商品Demo"""

    def run(self):
        try:

            c1 = ProductCategory(name='商品分类A')
            c2 = ProductCategory(name='商品分类B')
            c3 = ProductCategory(name='商品分类c')
            db.session.add_all([c1, c2, c3])
            db.session.commit()

            c1_id = c1.id
            c2_id = c2.id
            c3_id = c3.id

            for i in range(0, 9):
                cd = Product(
                    prod_category_id=random.choice([c1_id, c2_id, c3_id]),
                    name='商品:{}'.format(i),
                    summary='商品简介:{}'.format(i),
                    price=i
                )
                db.session.add(cd)
                db.session.commit()

            ak1 = AttributeKey(name='颜色')
            ak2 = AttributeKey(name='内存')
            ak3 = AttributeKey(name='版本')
            db.session.add_all([ak1, ak2, ak3])
            db.session.commit()

            ak1_id = ak1.id
            ak2_id = ak2.id
            ak3_id = ak3.id

            av_list = [
                AttributeVal(attr_key_id=ak1_id, name='红色'),
                AttributeVal(attr_key_id=ak1_id, name='蓝色'),
                AttributeVal(attr_key_id=ak1_id, name='绿色'),
                AttributeVal(attr_key_id=ak2_id, name='128G'),
                AttributeVal(attr_key_id=ak2_id, name='256G'),
                AttributeVal(attr_key_id=ak2_id, name='512G'),
                AttributeVal(attr_key_id=ak3_id, name='v1.0'),
                AttributeVal(attr_key_id=ak3_id, name='v2.0'),
                AttributeVal(attr_key_id=ak3_id, name='v3.0'),
                AttributeVal(attr_key_id=ak3_id, name='v4.0'),
                AttributeVal(attr_key_id=ak3_id, name='v5.0'),
                AttributeVal(attr_key_id=ak3_id, name='v6.0')
            ]
            for av in av_list:
                db.session.add(av)
            db.session.commit()

        except BaseException as e:
            print(str(e))


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


class CrmAdmin(Command):

    def run(self):
        if Admin.query.filter_by(username='yangyuexiong', is_deleted=0).first():
            raise ValueError('yangyuexiong 已经存在')
        else:
            admin = Admin(
                username='yangyuexiong',
                password='123456',
                phone='15013038819',
                mail='yangyuexiong33@gmail.com',
                code='00001',
                creator='shell',
                creator_id='0',
                remark='manage shell'
            )
            db.session.add(admin)
            db.session.commit()
            print('admin 创建完成')

        if Role.query.filter_by(name='超级管理员', is_deleted=0).first():
            raise ValueError('超级管理员 已经存在')
        else:
            role = Role(name='超级管理员', creator='shell', creator_id='0', remark='manage shell')
            db.session.add(role)
            db.session.commit()
            print('role 创建完成')

        api_resource = ApiResource(
            name='crm首页',
            url='/crm/index',
            method='GET',
            creator='shell',
            creator_id='0',
            remark='manage shell'
        )
        db.session.add(api_resource)
        db.session.commit()
        print('api_resource 创建完成')

        permission = Permission(
            name='yyx',
            resource_id=api_resource.id,
            resource_type='SERVER_API',
            creator='shell',
            creator_id='0',
            remark='manage shell'
        )
        db.session.add(permission)
        db.session.commit()
        print('permission 创建完成')

        mid_admin_role = MidAdminAndRole(
            admin_id=admin.id,
            role_id=role.id,
            creator='shell',
            creator_id='0',
            remark='manage shell'
        )
        db.session.add(mid_admin_role)
        db.session.commit()
        print('mid_admin_role 创建完成')

        mid_permission_role = MidPermissionAndRole(
            permission_id=permission.id,
            role_id=role.id,
            creator='shell',
            creator_id='0',
            remark='manage shell'
        )
        db.session.add(mid_permission_role)
        db.session.commit()
        print('mid_permission_role 创建完成')


# 添加命令
manager.add_command('hello', Hello())
manager.add_command('orm', TableCreateFirst())
manager.add_command('table', TableCreate())
manager.add_command('crm', CRMInit())
manager.add_command('admin', CrmAdmin())


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
