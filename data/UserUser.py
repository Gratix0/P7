import sqlalchemy
from sqlalchemy import orm
from .For_db import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Users(SqlAlchemyBase, SerializerMixin):
    """
    Создаёт модель таблицы
    """
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    role = sqlalchemy.Column(sqlalchemy.Integer)
