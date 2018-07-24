from sqlalchemy import Column, Integer, Boolean, DateTime
from conf import Session

import datetime


class BasicFormer(object):

    id = Column(type_=Integer, primary_key=True, autoincrement=True, doc="主键")

    obj_deleted = Column(type_=Boolean, default=False, nullable=False, doc="已删除")

    create_time = Column(type_=DateTime, default=datetime.datetime.now(), nullable=False, doc="创建时间")

    update_time = Column(
        type_=DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now, nullable=False, doc="更新时间"
    )

    def update(self, **kwargs):
        """
        更新实例信息
        :param kwargs: 
        :return: 
        """
        with Session() as session:
            for field, field_value in kwargs.items():
                setattr(self, field, field_value)
                session.add(self)
        return self

    def save(self):
        """
        保存实例
        :return: 
        """
        with Session() as session:
            session.add(self)
            raise TypeError("hello world")
        return self

    def delete(self, _real_deleted=False):
        """
        删除实例
        :param _real_deleted: 
        :return: 
        """
        with Session() as session:
            if _real_deleted:
                session.delete(self)
            else:
                self.obj_deleted = True
            session.add(self)
