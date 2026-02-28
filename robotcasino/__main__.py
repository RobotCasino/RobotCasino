
import sys, typer, rich, os, signal
import typing, datetime, multiprocessing

from tracemalloc import stop

from robotcasino.casinos import Magnater
from robotcasino.jarvis import Jarvis
from robotcasino.process import SocketServer
from robotcasino.scraper import Scraper
from robotcasino.ipc import Sender
from robotcasino.process import DaemonProcess, ForegroundProcess
from robotcasino.bootstrap import get_casino, get_environment
from robotcasino.constants import PID_PATH, SOCKET_PATH, OUTPUT_DIR

app = typer.Typer(add_completion=False)


def _run_scraper(gameName: str, casinoName: typing.Optional[str], strategyName: typing.Optional[str], extra_params: dict) -> None:
    try:
        strategyName = strategyName or 'default'
        casinoName = casinoName or 'one_win'

        casino = Magnater.get_casino(casinoName)

        game = casino.get_game(gameName) 

        game.set_strategy(strategyName)

        game.set_user_data(extra_params)

        scraper = Scraper(casino, game)

        socketServer = SocketServer(scraper.controller, scraper.run)

        return socketServer, scraper
    except Exception as e:
        Jarvis.error(str(e), e)

        os._exit(1)


def _parse_extra_params(ctx: typer.Context) -> dict:
    extra_params = {}
    if ctx.args:
        i = 0
        while i < len(ctx.args):
            arg = ctx.args[i]
            if arg.startswith('--'):
                key = arg.lstrip('--')
                if i + 1 < len(ctx.args) and not ctx.args[i + 1].startswith('--'):
                    extra_params[key] = ctx.args[i + 1]
                    i += 2
                else:
                    extra_params[key] = True
                    i += 1
            else:
                i += 1
    return extra_params


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    short_help="Run the Scraper in foreground mode (Docker-compatible)."
)
def run(ctx: typer.Context, fixture: str, casino: typing.Optional[str] = typer.Option(None, "--casino", "-c", help="Optional casino identifier"), strategy: typing.Optional[str] = typer.Option(None, "--strategy", "-s", help="Optional strategy to pass to the scraper")):
    """Run the scraper in the foreground. This is the recommended mode for Docker containers."""
    extra_params = _parse_extra_params(ctx)

    socketServer, scraper = _run_scraper(fixture, casino, strategy, extra_params)

    process = ForegroundProcess(socketServer.loop, scraper.close)

    Jarvis.info(f"Starting scraper in foreground mode — game={fixture}, casino={casino or 'one_win'}, strategy={strategy or 'default'}")

    process.start()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    short_help="Start the Scraper as a background daemon (not for Docker)."
)
def start(ctx: typer.Context, fixture: str, casino: typing.Optional[str] = typer.Option(None, "--casino", "-c", help="Optional casino identifier"), strategy: typing.Optional[str] = typer.Option(None, "--strategy", "-s", help="Optional strategy to pass to the scraper")):
    """Start the scraper as a background daemon. Not compatible with Docker — use 'run' instead."""
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
    
    extra_params = _parse_extra_params(ctx)

    socketServer, scraper = _run_scraper(fixture, casino, strategy, extra_params)

    daemon = DaemonProcess(socketServer.loop, scraper.close)
    daemon.start()

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
def screenshot(path: typing.Annotated[str, typer.Argument()] = None):
    if path is None:
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
        path = str(OUTPUT_DIR / filename)

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

        res = sender.send({
            "cmd": "status",
            "arguments": "",
        })

        if res is not None:
            rich.print(res.get("result"))
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