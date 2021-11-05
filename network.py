import asyncio
import hashlib
import struct
import sys
import time
from typing import Tuple
import json
from logger import logger
from db import get_dals
from db.config import engine, Base
from network_packets import Packet, unpack_packet
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

    async def new_connection(self, addr, name, save_db=False, priv_key: bytes = None):
        """

        :param addr:
        :param name:
        :param save_db: Save to database (you must specify the user's private key)
        :param priv_key:
        :return:
        """
        keys = self.keys.get_keys()
        if save_db:
            # TODO When the interface is ready, send a new user there
            dal = await get_dals.get_user_dal()
            await dal.create_user(name, addr, keys[0], keys[1], priv_key)
        else:
            self.temp_addr[addr] = (name, keys[0], keys[1])
        data = Packet('NKEY', keys[1]).build()
        await self.send(data, addr)

    async def send(self, msg: bytes, addr: str):
        reader, writer = await self.__open_connection(addr)
        writer.write(msg)
        await writer.drain()
        writer.close()


class Server:
    client: Client

    @classmethod
    async def create(cls, port: int, client: Client) -> "Server":
        self = Server()
        self.__server = await asyncio.start_server(self.__handle_data, '0.0.0.0', port)
        self.client = client
        return self

    async def __handle_data(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(-1)
        addr = writer.get_extra_info('peername')[0]
        logger.info(f'From {addr}: Get new message')
        try:
            data = unpack_packet(data)
        except struct.error:
            logger.error(f'From {addr}: Error while trying to unpack the message')
            return
        cmd, content_hash, _, content = data
        if cmd == b'NKEY':
            await self.__handle_new_conn(addr, content, content_hash)
        elif cmd == b'MESG':
            pass
        else:
            logger.error(f'From {addr}: Unknown cmd')

    async def __handle_new_conn(self, addr, content: bytes, c_hash: bytes):
        # Conditional check, because the hash can also be replaced
        if hashlib.sha256(content).digest() != c_hash:
            logger.error(f'From {addr}: Wrong hash')
            return
        if addr in self.client.temp_addr:
            dal = await get_dals.get_user_dal()
            user_info = self.client.temp_addr[addr]
            await dal.create_user(user_info[0], addr, user_info[1], user_info[2], content)
            logger.debug(f"Added new user in db {addr, user_info[0]}")
            return
        else:
            # How about adding a connection request?
            await self.client.new_connection(addr, addr, True, content)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    b = await Client.create(8888)
    a = await Server.create(8888, b)
    await asyncio.sleep(3)
    while True:
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    # Fucking windows ProactorEventLoop
    # I spent 4 hours figuring out what the problem is and fixing it
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
