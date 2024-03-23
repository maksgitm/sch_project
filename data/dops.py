import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin


class Dops(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'dops'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    speciality = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.String)
    cost = sqlalchemy.Column(sqlalchemy.String)
    qr_code = sqlalchemy.Column(sqlalchemy.BLOB)
