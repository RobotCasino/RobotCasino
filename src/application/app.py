
from typer import Typer

App = Typer(add_completion=False)

# Importing CLI commands #

import core.cli.run
import core.cli.stop
import core.cli.status
import core.cli.screenshot