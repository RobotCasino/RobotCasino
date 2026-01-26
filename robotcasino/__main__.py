
import logging
import sys, typer, rich, os, signal
import typing, datetime, multiprocessing

from tracemalloc import stop

from robotcasino.process import SocketServer
from robotcasino.scraper import Scraper
from robotcasino.ipc import Sender
from robotcasino.process import DaemonProcess
from robotcasino.bootstrap import get_casino, get_environment

from robotcasino.constants import PID_PATH, SOCKET_PATH

logger = logging.getLogger(__name__)

app = typer.Typer(add_completion=False)

def _run_scraper(gameName: str, casinoName: typing.Optional[str], strategyName: typing.Optional[str]) -> None:
    try:
        strategyName = strategyName or 'default'
        casinoName = casinoName or 'one_win'

        casino = get_casino(casinoName)

        game = casino.get_game(gameName) 

        game.set_strategy(strategyName)        

        scraper = Scraper(casino, game)

        socketServer = SocketServer(scraper.controller, scraper.run)
        daemon = DaemonProcess(socketServer.loop, scraper.close)

        daemon.start()
    except Exception as e:
        logger.error("Failed to start scraper", exc_info=True)
        
        os._exit(1)

@app.command(short_help="Start the Scraper process.")
def start(fixture: str, casino: typing.Optional[str] = typer.Option(None, "--casino", "-c", help="Optional casino identifier"), strategy: typing.Optional[str] = typer.Option(None, "--strategy", "-s", help="Optional strategy to pass to the scraper")):
    if DaemonProcess.is_running():
        try:
            rich.print(":warning: Scraper is already running.")
            desicion = typer.prompt("Do you want to stop it and start a new one? (y/n)")
        except Exception:
            os._exit(1)
        
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
        pass

    pidFile.unlink(missing_ok=True)

@app.command(short_help="Take a screenshot and save it to path.")
def screenshot(path: typing.Annotated[str, typer.Argument()] = ("./" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg")):
    try:
        sender = Sender(str(SOCKET_PATH))

        res = sender.send({
            "cmd": "screenshot",
            "arguments": path,
        })

        if res is not None:
            rich.print(res.get("result"))

    except Exception:
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
        rich.print(":warning: Unable to connect to the Scraper process. Is it running?", file=sys.stderr)

@app.command(short_help="Shows the HTML content of the current page.")
def html():
    try:
        sender = Sender(str(SOCKET_PATH))

        res = sender.send({
            "cmd": "get_html",
            "arguments": "",
        })

        if res is not None:
            print(res.get("result"))

    except Exception:
        rich.print(":warning: Unable to connect to the Scraper process. Is it running?", file=sys.stderr)


def main():
    app()


if __name__ == "__main__":
    main()