from sqlalchemy import Column, String

from apps.basic.abstract import DeclarativeBaseModel
from apps.tcenter.formers import BasicTaskFormer


class BasicTask(DeclarativeBaseModel, BasicTaskFormer):

    __tablename__ = "basic_task"

    task_name = Column(type_=String(length=30), nullable=False, doc="任务名称")

    def __repr__(self):

        return "{0}".format(self.task_name)
