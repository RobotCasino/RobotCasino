from ctypes import ArgumentError
import sys, typer, rich, os, signal
from rich.console import Console
import logging
from tracemalloc import stop
logger = logging.getLogger(__name__)
import typing, datetime, multiprocessing

import robotcasino.casinos as Casinos
import robotcasino.bootstrap
from robotcasino.casinos.strategies.strategier import Strategier
from robotcasino.process.socket_server import SocketServer
from robotcasino.scraper import Scraper
from robotcasino.ipc import Sender
from robotcasino.process import DaemonProcess

from robotcasino.constants import PID_PATH, SOCKET_PATH

app = typer.Typer(add_completion=False)

def _run_scraper(fixture: str, casino: typing.Optional[str], strategy: typing.Optional[str]) -> None:
    try:
        strategy = strategy or 'default'
        casino = casino or 'one_win'

        if fixture not in Casinos.Games:
            raise ArgumentError(f"Unsupported fixture: {fixture}")
        
        if not Strategier.is_strategy(casino, fixture, strategy):
            raise ArgumentError(f"Unsupported strategy: {strategy} for game: {fixture}")

        game = Casinos.Games[fixture](strategy)

        scraper = Scraper(game)

        socketServer = SocketServer(scraper.controller, scraper.run)
        daemon = DaemonProcess(socketServer.loop, scraper.close)

        daemon.start()
    except Exception as e:
        logger.error("Failed to start scraper", exc_info=True)
        os._exit(1)

@app.command(short_help="Start the Scraper process.")
def start(fixture: str, casino: typing.Optional[str] = typer.Option(None, "--casino", "-c", help="Optional casino identifier"), strategy: typing.Optional[str] = typer.Option(None, "--strategy", "-s", help="Optional strategy to pass to the scraper")):
    if DaemonProcess.is_running():

        rich.print(":warning: Scraper is already running.")
        desicion = typer.prompt("Do you want to stop it and start a new one? (y/n)")

        if desicion.lower() == 'y':
            stop()
        else:
            return

    proc = multiprocessing.Process(target=_run_scraper, args=(fixture, casino, strategy))
        
    proc.start()

@app.command(short_help="Stop the Scraper process.")
def stop():
    pidFile = PID_PATH

    if not pidFile.is_file():
        return

    pid = int(pidFile.read_text().strip())

    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pidFile.unlink(missing_ok=True)
        pass

@app.command(short_help="Take a screenshot and save it to path.")
def screenshot(path: typing.Annotated[str, typer.Argument()] = ("./" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg")):
    try:
        sender = Sender(str(SOCKET_PATH))

        sender.send({
            "cmd": "screenshot",
            "arguments": path,
        })
    except Exception:
        logger.error("Unable to connect to the Scraper process (screenshot)", exc_info=True)
        rich.print(":warning: Unable to connect to the Scraper process. Is it running?", file=sys.stderr)

@app.command(short_help="Shows the status of the Scraper process.")
def status():
    try:
        sender = Sender(str(SOCKET_PATH))

        sender.send({
            "cmd": "status",
            "arguments": "",
        })

    except Exception:
        logger.error("Unable to connect to the Scraper process (status)", exc_info=True)
        rich.print(":warning: Unable to connect to the Scraper process. Is it running?", file=sys.stderr)

def main():
    app()


if __name__ == "__main__":
    main()