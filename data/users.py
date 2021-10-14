import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ip = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_private_key = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_public_key = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_public_key_addr = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
