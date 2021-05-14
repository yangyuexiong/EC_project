# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 11:29
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : tools.py
# @Software: PyCharm

import json
import time
from datetime import datetime

from flask import request
from sqlalchemy import or_


def print_logs():
    """logs"""
    print(datetime.now())
    host = request.host
    print(host)
    method = request.method
    print(method)
    path = request.path
    print(path)
    print('=== headers ===')
    headers = {k: v for k, v in request.headers.items()}
    json_format(headers)
    print('=== params ===')
    json_format(request.args.to_dict())
    print('=== data ===')
    json_format(request.form.to_dict())
    print('=== json ===')
    json_format(request.get_json())


def check_keys(dic, *keys):
    for k in keys:
        if k not in dic.keys():
            return False
    return True


def json_format(d):
    """json格式打印"""
    try:
        print(json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
    except BaseException as e:
        print(d)


def gen_order_number():
    """生成订单号"""
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')
    return order_no


def general_paging_fuzzy_query(q, model, like_params, where_dict, page=1, size=20):
    """
    通用分页模糊查询
    :param q: 搜索内容
    :param model: 模型
    :param like_params: 模糊查询字段
    :param where_dict: 条件
    :param page: 页码
    :param size: 条数
    :return:
    """
    print(q, model, like_params, where_dict)
    where_list = []
    if where_dict:
        for k, v in where_dict.items():
            if hasattr(model, k):
                where_list.append(getattr(model, k) == v)

    like_list = []
    for k, v in model.__dict__.items():
        if k in like_params:
            # print(k, type(k), '======', v, type(v))
            like_list.append(v.ilike(q if q is not None else ''))  # 模糊条件
    pagination = model.query.filter(or_(*like_list), *where_list).order_by(model.create_time.desc()).paginate(
        page=int(page),
        per_page=int(size),
        error_out=False
    )
    # result_list = []
    # for i in pagination.items:
    #     obj = i.to_json()
    #     result_list.append(obj)

    result_list = [i.to_json() for i in pagination.items]
    return result_list
