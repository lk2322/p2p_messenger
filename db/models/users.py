import datetime
import sqlalchemy
import sqlalchemy_utils
from db.config import Base


class Users(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ip = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_private_key = sqlalchemy.Column(
        sqlalchemy_utils.PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt']), nullable=True)
    hashed_public_key = sqlalchemy.Column(
        sqlalchemy_utils.PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt']), nullable=True)
    hashed_public_key_addr = sqlalchemy.Column(
        sqlalchemy_utils.PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt']), nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
