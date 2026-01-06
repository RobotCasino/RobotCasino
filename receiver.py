import json


class Receiver:

    def __init__(self, reader, writer):
        self.data = json.loads(scrumbled_data.decode())
        
        self.reader = reader
        self.writer = writer

        if self.__check() is False:
            raise ValueError("Invalid receiver data.")

    def get_command(self) -> str:
        return self.data.get("cmd", None)
    
    def get_parameters(self) -> dict:
        return self.data.get("params", None)

    def __check(self) -> bool:
        return not (self.data is None or not "cmd" in self.data or not "params" in self.data)
    
    def close(self) -> None:
        self.writer.close()