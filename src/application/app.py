import rich
from datetime import datetime

from typer import Typer, Context
from application.scraper import Scraper
from infrastructure.ipc.sender import Sender
from infrastructure.process.socket_server import SocketServer
from infrastructure.process.foreground import ForegroundProcess
from common.utils.args_parser import ArgsParser

from common.constants.directories import DOWNLOAD_DIR

App = Typer(add_completion=False)

@App.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    short_help="Run the Scraper in foreground mode (Docker-compatible)."
)
def run(ctx: Context, browser: str, casino: str, game: str, strategy: str):
    extra_params = ArgsParser.parse_args(ctx.args)

    scraper = Scraper(browser, casino, game, strategy, extra_params)

    socketServer = SocketServer(scraper.controller, scraper.run)

    process = ForegroundProcess(socketServer.loop, scraper.close)

    process.start()

@App.command(
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
    short_help="Take a screenshot and save it to the path."
)
def screenshot(filename: str | None = None):
    path = filename or datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"

    res = Sender.send({
        "cmd": "screenshot",
        "arguments": f"{DOWNLOAD_DIR}{path}",
    })

    if res is not None:
        rich.print(res.get("result"))

@App.command(
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
    short_help="Stop the scraper and exit."
)
def stop():
    Sender.send({
        "cmd": "stop",
    })

@App.command(
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
    short_help="Get the current status of the scraper."
)
def status():
    res = Sender.send({
        "cmd": "status",
    })

    if res is not None:
        rich.print(res.get("result"))