# -*- coding: utf-8 -*-
# @Time    : 2021/5/28 下午5:22
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class Order(BaseModel):
    __tablename__ = 'ec_order'
    __table_args__ = {'comment': '订单表'}
