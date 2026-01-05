import asyncio
import multiprocessing
from time import sleep
import typer
from rich import print
from pathlib import Path
import os
import signal
import sys

from robot import Robot

app = typer.Typer(add_completion=False)

def _run_robot() -> None:
    try:
        pid = os.fork()
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

    pidPath = Path('./run/robot.pid')

    pidPath.parent.mkdir(parents=True, exist_ok=True)

    pidPath.write_text(str(os.getpid()))

    def handle_terminate(signum, frame):
        print(":robot: Turning off robot...")
        pidPath.unlink(missing_ok=True)
        os.killpg(int(os.getpid()), signal.SIGKILL)

    signal.signal(signal.SIGINT, handle_terminate)
    signal.signal(signal.SIGTERM, handle_terminate)
    
    sleep(10)
    
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
        print(":rocket: Starting robot...")
        pidFile.parent.mkdir(parents=True, exist_ok=True)

        proc = multiprocessing.Process(target=_run_robot)
        proc.start()
        pidFile.write_text(str(proc.pid))


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
def screenshot(path: str):
    print(":warning: Taking screenshot...")

if __name__ == "__main__":
    asyncio.run(app())