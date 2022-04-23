import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Bucket(SqlAlchemyBase):
    __tablename__ = 'buckets'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    short_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    full_html = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer,
                              index=True, unique=True, nullable=True)
    pic_url = sqlalchemy.Column(sqlalchemy.Integer,
                              index=True, unique=True, nullable=True)
    machine_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("machines.id"))
    machine = orm.relation("Machine")