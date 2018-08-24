from sqlalchemy import Column, Integer, Boolean, DateTime
from conf import SessionContext

import datetime


class BasicFormer(object):

    id = Column(type_=Integer, primary_key=True, autoincrement=True, doc="主键")

    obj_deleted = Column(type_=Boolean, default=False, nullable=False, doc="已删除")

    create_time = Column(type_=DateTime, default=datetime.datetime.now(), nullable=False, doc="创建时间")

    update_time = Column(
        type_=DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now, nullable=False, doc="更新时间"
    )

    def serializer(self, skip_fields=None, extra_fields=None):
        """
        序列化对象
        :param skip_fields:
        :param extra_fields:
        :return:
        """
        if not skip_fields:
            skip_fields = []

        if not extra_fields:
            extra_fields = []

        data = {}

        for field in self.__class__.__table__.columns.keys():
            if field in skip_fields:
                continue

            value = self.__getattribute__(field)

            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            data[field] = value

        for field in extra_fields:
            data[field] = self.__getattribute__(field)

        return data

    def update(self, **kwargs):
        """
        更新实例信息
        :param kwargs: 
        :return: 
        """
        with SessionContext() as session:
            for field, field_value in kwargs.items():
                setattr(self, field, field_value)
                session.add(self)
        return self

    def save(self):
        """
        保存实例
        :return: 
        """
        with SessionContext() as session:
            session.add(self)
        return self

    def delete(self, _real_deleted=False):
        """
        删除实例
        :param _real_deleted: 
        :return: 
        """
        with SessionContext() as session:
            if _real_deleted:
                session.delete(self)
            else:
                self.obj_deleted = True
            session.add(self)
