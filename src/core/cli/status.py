from rich import print

from infrastructure.ipc.sender import Sender
from application.app import App

@App.command(
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
    short_help="Get the current status of the scraper."
)
def status():
    res = Sender.send({
        "cmd": "status",
    })

    if res is not None:
        print(res.get("result"))