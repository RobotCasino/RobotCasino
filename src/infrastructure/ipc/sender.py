import json
from socket import AF_UNIX, SOCK_STREAM, socket
from typing import Optional

from common.constants.directories import TMP_DIR

class Sender:
    __SOCKET_PATH = TMP_DIR + ".robotcasino.socket"

    @staticmethod
    def send(message: dict[str, str]) -> Optional[dict[str, str]]:
        with socket(AF_UNIX, SOCK_STREAM) as client:
            client.connect(Sender.__SOCKET_PATH)
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
