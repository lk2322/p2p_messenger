from data import db_session
from data.users import User


class DB:
    def __init__(self, db_name):
        db_session.global_init(db_name)

    def __add_model(self, model):
        db_sess = db_session.create_session()
        db_sess.add(model)
        db_sess.commit()
        db_sess.close()

    def add_user(self, name: str, ip: str, priv_key: str, pub_key: str, pub_key_user: str) -> None:
        """""
        name: Contact name
        ip: IPv4/v6 address of user
        priv_key: Private key of sender
        pub_key: Public key of sender
        pub_key_user: Public key of recipient
        """""
        contact = User(name=name, ip=ip, hashed_private_key=priv_key, hashed_public_key=pub_key,
                       hashed_public_key_addr=pub_key_user)
        self.__add_model(contact)

    def del_user(self, user_id: int) -> None:
        pass

    def edit_user(self, user_id: int) -> None:
        pass


if __name__ == "__main__":
    a = DB('123.db')
    a.add_user('asd', 'asd', 'asd', 'asd', 'asd')
