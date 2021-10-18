import asyncio


class Server:
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.server = asyncio.start_server(self.handle_msg, '127.0.0.1', 8888, loop=loop)

    async def handle_msg(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(100)


class Client:
    def __init__(self, loop):
        self.loop = loop

    async def __open_connection(self):
        return await asyncio.open_connection('127.0.0.1', 8888, loop=self.loop)

    async def send(self, msg):
        reader, writer = await self.__open_connection()
        writer.write(msg)
