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
    order_number = db.Column(db.String(128), comment='订单号')
    out_order_number = db.Column(db.String(128), comment='第三方订单号')
    user_id = db.Column(BIGINT(20, unsigned=True), comment='用户id')
    mobile = db.Column(db.String(64), comment='用户手机号')
    logistics_number = db.Column(db.String(64), comment='物流单号')
    order_type = db.Column(db.String(32), server_default=text('NORMAL'), comment='订单类型')
    user_remark = db.Column(db.String(128), comment='用户备注')
