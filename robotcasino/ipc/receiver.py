import json
from enum import Enum
from asyncio import StreamReader

class CommandTypeEnum(Enum):
    START = "start"
    STOP = "stop"
    SCREENSHOT = "screenshot"

class Receiver:

    def __init__(self, reader: StreamReader, data: dict):
        self.reader = reader
        self.data = data

    @classmethod
    async def create(cls, reader: StreamReader):
        data = await cls.__load_data(reader)
        return cls(reader, data)

    def get_command(self) -> str:
        return self.data.get("cmd", "")
    
    def get_parameters(self) -> str:
        return self.data.get("arguments", "")
    
    @staticmethod
    async def __load_data(reader: StreamReader) -> dict:
        data = await reader.readline()

        if not data:
            raise ValueError("No data received")
        
        msg = json.loads(data.decode().strip())

        if not isinstance(msg, dict):
            raise ValueError("Invalid data format")

        response: dict = {
            "cmd": msg.get("cmd", ""),
            "arguments": msg.get("arguments"),
        }

        return response


__ALL__ = ["Receiver", "CommandTypeEnum"]