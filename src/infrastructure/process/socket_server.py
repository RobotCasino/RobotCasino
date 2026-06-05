from genericpath import isfile
from os import path, remove

from asyncio import StreamReader, StreamWriter, gather, start_unix_server
from typing import Awaitable, Callable

from common.constants.directories import TMP_DIR

class SocketServer:
    def __init__(self, listener: Callable[[StreamReader, StreamWriter], Awaitable[None] | None], program: Callable[[], Awaitable[None]]):
        self.listener = listener
        self.program = program

        self.socketFilePath = TMP_DIR + ".robotcasino.socket"
    
    async def start_unix_server(self):
        return await start_unix_server(self.listener, self.socketFilePath)
    
    async def loop(self):
        if path.exists(self.socketFilePath):
            remove(self.socketFilePath)

        server = await start_unix_server(self.listener, str(self.socketFilePath))

        try:
            await gather(self.program(), server.serve_forever())
        finally:
            server.close()
            
            await server.wait_closed()

            if path.isfile(self.socketFilePath):
                remove(self.socketFilePath)
