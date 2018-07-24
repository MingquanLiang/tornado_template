from sqlalchemy.ext.declarative import declarative_base
from apps.basic.formers import BasicFormer

DeclarativeBaseModel = declarative_base(cls=BasicFormer)
