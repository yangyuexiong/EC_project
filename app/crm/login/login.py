# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午5:23
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : login.py
# @Software: PyCharm

from app.all_reference import *
from app.models.admin.models import Admin


class LoginCrmApi(Resource):
    """
    login
    POST: 登录
    DELETE: 退出
    """

    def post(self):
        data = request.get_json()
        if check_keys(data, 'username', 'password'):
            username = data.get('username', '')
            password = data.get('password', '')
            admin = Admin.query.filter_by(username=username).first()
            if admin and admin.check_password(password):
                """
                检查是否存在旧token并且生成新token覆盖旧token,或创建一个新的token。然后添加至返回值。
                """
                admin_obj = admin.to_json(*['_password'])
                t = Token()
                t.check_token(user=admin.username, user_id=admin.id)
                admin_obj['token'] = t.token
                return api_result(code=200, message='登录成功', data=admin_obj)
            else:
                return api_result(code=200, message='用户不存在或密码错误', data=[])
        else:
            ab_code_2(1000001)

    def delete(self):
        # print(request.headers.get('Token'))
        Token.del_token(request.headers.get('Token'))
        return api_result(code=204, message='退出成功')
