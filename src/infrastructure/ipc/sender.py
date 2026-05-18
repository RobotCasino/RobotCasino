import json
from socket import AF_UNIX, SOCK_STREAM, socket
from typing import Optional

class Sender:

    def __init__(self, socketPath: str):
        self.__socketPath = socketPath

    def send(self, message: dict[str, str]) -> Optional[dict[str, str]]:
        with socket(AF_UNIX, SOCK_STREAM) as client:
            client.connect(self.__socketPath)
            client.sendall((json.dumps(message) + "\n").encode())

            data = b""
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b"\n" in chunk:
                    break

        if data:
            return json.loads(data.decode().strip())
        return None
    
__ALL__ = ["Sender"]
