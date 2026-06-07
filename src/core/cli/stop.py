from infrastructure.ipc.sender import Sender
from application.app import App

@App.command(
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
    short_help="Stop the scraper and exit."
)
def stop():
    Sender.send({
        "cmd": "stop",
    })