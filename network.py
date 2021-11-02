import asyncio
import sys
import time
from typing import Tuple
import json
from logger import logger

from db.config import engine, Base
from network_packets import Packet
from rsa import Keys


class Client:
    @classmethod
    async def create(cls, port) -> "Client":
        self = Client(port)
        return self

    def __init__(self, port):
        self.port = port
        self.keys = Keys()
        self.temp_addr = {}  # {addr: (name, priv_key, pub_key)}

    async def __open_connection(self, adr: str) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """
        Opens a connection and returns Reader, Writer

        :param adr: Address of the recipient
        :return: (StreamReader, StreamWriter)
        """
        return await asyncio.open_connection(adr, self.port)

    async def new_connection(self, addr, name):
        keys = self.keys.get_keys()
        self.temp_addr[addr] = (name, keys[0], keys[1])
        data = Packet('NKEY', keys[1]).build()
        await self.send(data, addr)

    async def send(self, msg, adr):
        reader, writer = await self.__open_connection(adr)
        writer.write(msg)
        await writer.drain()
        writer.close()


class Server:
    @classmethod
    async def create(cls, port: int, client: Client) -> "Server":
        self = Server()
        self.__server = await asyncio.start_server(self.__handle_msg, '0.0.0.0', port)
        self.client = client
        return self

    async def __handle_msg(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(-1)
        decoded_data = data.decode()
        addr = writer.get_extra_info('peername')[0]
        logger.info(f"From {addr}: Get new message")
        try:
            msg: dict = json.loads(decoded_data)
        except json.JSONDecodeError:
            logger.error(f"From {addr}: Error decoding json from message")
            return
        if msg.get('new_connection'):
            pass  # TODO Создание нового соединения
        if msg.get("message"):
            pass  # TODO Обработка сообщений


async def main():
    b = await Client.create(8888)
    a = await Server.create(8888, b)
    await b.send(b'{}', "127.0.0.1")
    while True:
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    # Fucking windows ProactorEventLoop
    # I spent 4 hours figuring out what the problem is and fixing it
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
