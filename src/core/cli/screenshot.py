
from rich import print
from datetime import datetime

from common.constants.directories import SCREENSHOT_DIR
from infrastructure.ipc.sender import Sender
from application.app import App

@App.command(
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
    short_help="Take a screenshot and save it to the path."
)
def screenshot(filename: str | None = None):
    path = filename or datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"

    res = Sender.send({
        "cmd": "screenshot",
        "arguments": f"{SCREENSHOT_DIR}{path}",
    })

    if res is not None:
        print(res.get("result"))