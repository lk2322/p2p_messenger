import asyncio
import time
from typing import Tuple
import json
from logger import logger

from db.config import async_session, engine, Base

from db.dals.users_dal import UserDAL
from rsa import Keys



class Client:
    @classmethod
    async def create(cls, port) -> "Client":
        return Client(port)

    def __init__(self, port):
        self.port = port
        self.keys = Keys()

    async def __open_connection(self, adr: str) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """
        Opens a connection and returns Reader, Writer

        :param adr: Address of the recipient
        :return: (StreamReader, StreamWriter)
        """
        return await asyncio.open_connection(adr, self.port)

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
    c = Keys()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        async with session.begin():
            book_dal = UserDAL(session)
            await book_dal.create_user('asd', '123.1.2.1', b'asdadfsdf', b'asdasd', b'afsadfsdf')
    await b.send(b'a', "127.0.0.1")
    while True:
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())
