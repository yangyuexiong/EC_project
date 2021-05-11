# -*- coding: utf-8 -*-
# @Time    : 2019-05-16 17:06
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : BaseModel.py
# @Software: PyCharm

import json
from datetime import datetime

from ExtendRegister.db_register import db


class BaseModel(db.Model):
    """
    status:状态
    create_timestamp:创建时间戳
    create_time:创建时间DateTime
    update_timestamp:更新时间戳
    update_time:更新时间DateTime
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='id')
    status = db.Column('status', db.Integer, default=1, comment='状态:1正常,2删除')
    create_time = db.Column('create_time', db.DateTime, default=datetime.now, comment='创建时间(结构化时间)')
    create_timestamp = db.Column('create_timestamp', db.String(128), default=int(datetime.now().timestamp()),
                                 comment='创建时间(时间戳)')
    update_time = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now,
                            comment='更新时间(结构化时间)')
    update_timestamp = db.Column('update_timestamp', db.String(128), server_default='',
                                 onupdate=int(datetime.now().timestamp()), comment='更新时间(时间戳)')

    def keys(self):
        """
        返回所有字段对象
        :return:
        """
        return self.__table__.columns

    def __getitem__(self, item):
        return getattr(self, item)

    def to_json(self):

        """
        旧方法
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
            del dict["_update_timestamp"]
            del dict["_create_timestamp"]
            del dict["_create_time"]
            del dict["_update_time"]
            del dict["_status"]
            if str(self.__table__) == 'cms_user':
                del dict["_password"]
        """

        d = {}
        dict = self.__dict__
        [d.update({i.name: dict.get(i.name, '')}) for i in self.keys()]
        # print(d)

        d['create_time'] = str(d.get('create_time')) if d.get('create_time') else None
        d['update_time'] = str(d.get('update_time')) if d.get('update_time') else None

        # del d["update_timestamp"]
        # del d["create_timestamp"]
        # del d["create_time"]
        # del d["update_time"]
        # del d["status"]

        return d

    def update(self, **kwargs):
        # print('self->', self)
        for attr, value in kwargs.items():
            # print(self, attr, type(attr), value, type(value))
            try:  # 部分属性无法setattr
                setattr(self, attr, json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else str(value))
            except BaseException as e:
                print('update error {}'.format(str(e)))
        return self

    def delete_obj(self):
        self.status = 2
        db.session.commit()
