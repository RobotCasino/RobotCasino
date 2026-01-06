import asyncio
from datetime import date
import datetime
from http import server
import json
import multiprocessing
import sys
from typing import Annotated, Optional
import typer
from rich import print
from pathlib import Path
import os
import signal
from socket import socket, SOCK_STREAM, AF_UNIX
from datetime import datetime
from receiver import Receiver
from robot import Robot
from sender import Sender

app = typer.Typer(add_completion=False)

socketPath = Path('/tmp/robot_socket')
sender = Sender(str(socketPath))

def _run_robot() -> None:
    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError:
        pass

    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError:
        pass
    
    os.setpgid(0, 0)
    os.umask(0)

    my_robot = Robot()

    pidPath = Path('./run/robot.pid')

    pidPath.parent.mkdir(parents=True, exist_ok=True)

    pidPath.write_text(str(os.getpid()))

    async def handle_client(reader, writer):
        try:
            receiver = Receiver(reader, writer)

        except ValueError:
            pass
        finally:
            writer.close()
            await writer.wait_closed()
        try:
            data = await reader.readline()
            if not data:
                return
            msg = json.loads(data.decode().strip())
            cmd = msg.get("cmd")
            if cmd == "screenshot":
                path = msg.get("path")
                
                if path.endswith((".jpg", ".jpeg", ".png")) is False:
                    path += ".jpg"

                await my_robot.screenshot(path)
                writer.write(b'{"status":"ok"}\n')
            else:
                writer.write(b'{"status":"unknown_command"}\n')
            await writer.drain()
        except Exception as e:
            writer.write(f'{{"status":"error", "message": "{str(e)}"}}\n'.encode())
        finally:
            writer.close()
            await writer.wait_closed()

    async def main_loop():
        if socketPath.is_socket():
            socketPath.unlink(missing_ok=True)
        
        server = await asyncio.start_unix_server(handle_client, path=str(socketPath))
        try:
            await asyncio.gather(my_robot.run(), server.serve_forever())
        finally:
            server.close()
            await server.wait_closed()
            socketPath.unlink(missing_ok=True)

    def handle_terminate(signum, frame):
        asyncio.create_task(my_robot.close())
       
        pidPath.unlink(missing_ok=True)
        socketPath.unlink(missing_ok=True)
       
        os.killpg(int(os.getpid()), signal.SIGKILL)

    signal.signal(signal.SIGINT, handle_terminate)
    signal.signal(signal.SIGTERM, handle_terminate)

    asyncio.run(main_loop())

@app.command(short_help="Start the robot process.")
def start():
    pidFile = Path('./run/robot.pid')

    if pidFile.is_file():

        print(":warning: Robot is already running.")
        desicion = typer.prompt("Do you want to stop it and start a new one? (y/n)")

        if desicion.lower() == 'y':
            print(":information_source: Aborting.")
            stop()
        else:
            return

    else:
        pidFile.parent.mkdir(parents=True, exist_ok=True)

        proc = multiprocessing.Process(target=_run_robot)
        proc.start()


@app.command(short_help="Stop the robot process.")
def stop():
    pidFile = Path('./run/robot.pid')
    if not pidFile.is_file():
        return

    pid = int(pidFile.read_text().strip())

    try:
        os.killpg(pid, signal.SIGTERM)
    except OSError:
        pidFile.unlink(missing_ok=True)

@app.command(short_help="Take a screenshot and save it to path.")
def screenshot(path: Annotated[str, typer.Argument()] = ("./" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg")):
    try:
        res = sender.send({
            "cmd": "screenshot",
            "path": path
        })

        print(":white_check_mark: Screenshot saved to [bold]{0}[/bold].".format(path))
    except Exception:
        print(":warning: Unable to connect to the robot process. Is it running?", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(app())