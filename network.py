import socket
import typing
from db_control import DB
from threading import Thread
from typing import Union
import json
from data import db_session
import rsa


class P2P:
    def __init__(self, port: int = 5700, max_clients: int = 1):
        self.port = port
        self.max_clients = max_clients
        self.client_sockets = [socket.socket() for i in range(self.max_clients)]
        Thread()
        self.socket_busy = [False for i in range(self.max_clients)]
        self.server_socket = socket.socket()
        self.server_socket.bind(('localhost', self.port))
        self.server_socket.listen(self.max_clients)
        self.db = DB('main.db')
        Thread(self.__accept_connection()).start()

    def __accept_connection(self) -> None:
        """Wait connection. Run in Thread"""
        while True:
            conn, addr = self.server_socket.accept()
            # TODO Добавить логгирование
            data = conn.recv(1024)
            try:
                info = json.loads(data)
            except json.loads(data):
                continue
                # TODO Логи
            if info.get("new_connection"):
                # TODO функция обмена ключами и добавление в контакты
                pass
            elif info.get("message"):
                # TODO Рассшифровка сообщения
                pass
            # Нужно подумать над удалением чатов
            # elif info.get("del_chat"):
            #     pass
            for i in task:
                i()

    def __connect(self, adr: str):
        index = self.__get_free_socket()
        c_sock = self.client_sockets[index]
        c_sock.connect((adr, self.port))
        self.socket_busy[index] = True
        return c_sock, index

    def key_send(self, adr: str):
        c_sock, index = self.__connect(adr)
        key = rsa.newkeys(1024)
        message = {"new_connection": {"o_key": key[0].save_pkcs1()}}
        c_sock.send(bytes(json.dumps(message)))
        c_sock.close()
        self.socket_busy[index] = False

    def key_receive(self, adr: str, name: str) -> None:
        c_sock, index = self.__connect(adr)
        key = rsa.newkeys(1024)
        message = {"new_connection": {"o_key": key[0].save_pkcs1()}}
        c_sock.send(bytes(json.dumps(message)))
        data: dict = json.loads(c_sock.recv(1024).decode())
        if data.get("new_connection"):
            o_key = data.get("new_connection").get("o_key")
            self.db.add_user(name, adr, str(key[1].save_pkcs1()), str(key[0].save_pkcs1()), o_key)
        elif data.get("error"):
            pass
            # TODO Обработка ошибок

        c_sock.close()

        self.socket_busy[index] = False

    def __get_free_socket(self) -> Union[int, None]:
        """Returns the index of a free socket. Returns None if there are no free sockets"""
        for index, i in enumerate(self.socket_busy):
            if not i:
                return index
        return None


if __name__ == "__main__":
    P2P()
