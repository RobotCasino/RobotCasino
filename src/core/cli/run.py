from typer import Context

from application.app import App
from application.scraper import Scraper
from infrastructure.process.socket_server import SocketServer
from infrastructure.process.foreground import ForegroundProcess
from common.utils.args_parser import ArgsParser
    
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