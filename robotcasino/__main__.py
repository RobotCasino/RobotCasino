import asyncio, sys, typer, rich, pathlib, os, signal
import typing, datetime, multiprocessing

from robotcasino.scraper import Scraper
from robotcasino.ipc import Sender
from robotcasino.ipc import Receiver
from robotcasino.process import DaemonProcess

from .constants import PID_PATH, SOCKET_PATH

app = typer.Typer(add_completion=False)

def _run_scraper() -> None:
    scraper = Scraper()

    async def handle_terminate():
        await scraper.close()
    
    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            receiver = await Receiver.create(reader)

            commmand = receiver.get_command()
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def socket_loop():
        SOCKET_PATH.unlink(missing_ok=True)
        
        server = await asyncio.start_unix_server(handle_client, path=str(SOCKET_PATH))
        
        try:
            await asyncio.gather(scraper.run(), server.serve_forever())
        finally:
            server.close()
            await server.wait_closed()
            SOCKET_PATH.unlink(missing_ok=True)
    
    daemon = DaemonProcess(socket_loop, handle_terminate)
    
    try:
        daemon.start()
    except RuntimeError as e:
        rich.print(f":warning: Unable to daemonize process: {e}", file=sys.stderr)
        sys.exit(1)


@app.command(short_help="Start the Scraper process.")
def start():
    pidFile = PID_PATH

    if pidFile.is_file():

        rich.print(":warning: Scraper is already running.")
        desicion = typer.prompt("Do you want to stop it and start a new one? (y/n)")

        if desicion.lower() == 'y':
            rich.print(":information_source: Aborting.")
            stop()
        else:
            return

    else:
        pidFile.parent.mkdir(parents=True, exist_ok=True)

        proc = multiprocessing.Process(target=_run_scraper)
        proc.start()


@app.command(short_help="Stop the Scraper process.")
def stop():
    pidFile = PID_PATH

    if not pidFile.is_file():
        return

    pid = int(pidFile.read_text().strip())

    os.killpg(pid, signal.SIGTERM)


@app.command(short_help="Take a screenshot and save it to path.")
def screenshot(path: typing.Annotated[str, typer.Argument()] = ("./" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg")):
    try:
        sender = Sender(str(SOCKET_PATH))

        res = sender.send({
            "cmd": "screenshot",
            "arguments": path,
        })


    except Exception:
        rich.print(":warning: Unable to connect to the Scraper process. Is it running?", file=sys.stderr)


def main():
    app()


if __name__ == "__main__":
    main()