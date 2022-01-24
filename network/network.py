import abc
import asyncio
from asyncio import StreamWriter, StreamReader
from typing import Dict, Callable, List

from network_packets import unpack_packet

PORT = 12342


class Connection:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    rsa_key_priv: bytes
    rsa_key_public: bytes
    addr: str
    process_task: asyncio.Task
    handlers: List[Callable]

    @classmethod
    @abc.abstractmethod
    async def create_connection(cls, addr, writer: StreamWriter = None,
                                reader: StreamReader = None) -> 'Connection':
        conn = cls()
        conn.addr = addr
        conn.reader = reader
        conn.writer = writer
        await conn.run()
        return conn

    async def send(self, content):
        self.writer.write(content)
        await self.writer.drain()

    async def _handle(self, data: bytes):
        msg = unpack_packet(data)

        for func in self.handlers:
            func(self.addr, msg)

    async def run(self):
        if not (self.writer and self.reader):
            self.reader, self.writer = await asyncio.open_connection(self.addr, PORT)
            self.process_task = asyncio.create_task(self._run())

    async def _run(self):
        while True:
            try:
                next_message = await self.reader.read(2048)
            except ConnectionError:
                break
            if next_message == b'':
                break
            await self._handle(next_message)
            await asyncio.sleep(0.1)

    @property
    def is_alive(self) -> bool:
        return not self.process_task.done()


class Network:
    @classmethod
    async def create(cls):
        self = cls()
        self.__server = await asyncio.start_server(self.add_connection, host='0.0.0.0', port=PORT)
        return self

    def __init__(self):
        self.connections: Dict[str, Connection] = {}
        self.handlers: List = []

    async def add_handler(self, func):
        """
        Adds a handler for handling messages
        :param func: Receive addr, message
        :return:
        """
        self.handlers.append(func)

    async def connect(self, addr: str) -> Connection:
        connection = await Connection.create_connection(addr, handlers=self.handlers)
        self.connections[addr] = connection
        return connection

    async def add_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        conn = await Connection.create_connection(addr, self.handlers, writer, reader)
        self.handlers[addr] = conn

    async def send(self, addr, content):
        conn = self.handlers[addr]
        if conn.is_alive:
            return await self.handlers[addr].send(content)
        else:
            await self.connect(addr)
            return await self.handlers[addr].send(content)


if __name__ == '__main__':
    asyncio.run(Network.create())
