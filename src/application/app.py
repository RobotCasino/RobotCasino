from datetime import datetime

import rich

from typer import Typer, Context
from src.application.scraper import Scraper
from src.infrastructure.config import OUTPUT_DIR, SOCKET_PATH
from src.infrastructure.ipc.sender import Sender
from src.infrastructure.process.socket_server import SocketServer
from src.infrastructure.process.foreground import ForegroundProcess
from src.utils.args_parser import ArgsParser

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
def screenshot(path: str | None = None):
    path = path or datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    
    sender = Sender(SOCKET_PATH)

    res = sender.send({
        "cmd": "screenshot",
        "arguments": f"{OUTPUT_DIR / path}",
    })

    if res is not None:
        rich.print(res.get("result"))

@App.command(
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
    short_help="Stop the scraper and exit."
)
def stop():
    sender = Sender(SOCKET_PATH)

    sender.send({
        "cmd": "stop",
    })