from sqlalchemy import Column, String

from apps.basic.abstract import DeclarativeBaseModel


class NewApp(DeclarativeBaseModel):

    __tablename__ = "new_app"

    name = Column(type_=String(length=30), nullable=False, doc="名称")

    def __repr__(self):

        return "{0}".format(self.name)
