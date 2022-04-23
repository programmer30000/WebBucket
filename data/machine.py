import datetime
import sqlalchemy
from sqlalchemy import Column,Integer,String
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Machine(SqlAlchemyBase):
    __tablename__ = 'machines'

    #код
    id = Column(Integer,
                           primary_key=True, autoincrement=True)
    #тип техники
    type = Column(String, nullable=True)
    #пиктограмма в виде ссылки
    icon = Column(String, nullable=True)
    #картинка
    main_pic = Column(String, nullable=True)

    buckets = orm.relation("Bucket", back_populates='machine')

