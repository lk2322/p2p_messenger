import datetime
import sqlalchemy
from db.config import Base


class Users(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ip = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    private_key = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    public_key = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    public_key_addr = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
