from asyncio import StreamReader, StreamWriter, gather, start_unix_server
from typing import Awaitable, Callable

from src.infrastructure.config import SOCKET_PATH
from os import remove

class SocketServer:

    def __init__(self, listener: Callable[[StreamReader, StreamWriter], Awaitable[None] | None], program: Callable[[], Awaitable[None]]):
        self.listener = listener
        self.program = program
    
    async def start_unix_server(self):
        return await start_unix_server(self.listener, SOCKET_PATH)
    
    async def loop(self):
        remove(SOCKET_PATH)
        
        server = await start_unix_server(self.listener, str(SOCKET_PATH))

        try:
            await gather(self.program(), server.serve_forever())
        finally:
            server.close()
            
            await server.wait_closed()
            
            remove(SOCKET_PATH)
