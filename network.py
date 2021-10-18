import asyncio


class Server:
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.server = asyncio.start_server(self.handle_msg, '127.0.0.1', 8888, loop=loop)

    async def handle_msg(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(100)


class Client:
    pass
