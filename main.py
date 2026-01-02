import asyncio
import multiprocessing
import typer
from rich import print
from pathlib import Path
import os
import signal
import sys

from robot import Robot

app = typer.Typer(add_completion=False)

def _run_robot() -> None:
    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError:
        pass

    try:
        os.setsid()
    except Exception:
        pass

    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError:
        pass

    try:
        os.setpgid(0, 0)
    except Exception:
        pass

    log_dir = Path("run")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "robot.log"

    pid_file = log_dir / "robot.pid"
    try:
        pid_file.write_text(str(os.getpid()))
    except Exception:
        pass
    f = open(log_file, "a+", buffering=1)
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception:
        pass
    try:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())
        devnull = open(os.devnull, "r")
        os.dup2(devnull.fileno(), sys.stdin.fileno())
    except Exception:
        sys.stdout = f
        sys.stderr = f

    async def _daemon_main():
        my_robot = Robot()

        async def _shutdown():
            try:
                await my_robot.close()
            finally:
                for task in asyncio.all_tasks():
                    if task is not asyncio.current_task():
                        task.cancel()

        loop = asyncio.get_running_loop()
        try:
            loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(_shutdown()))
        except Exception:
            pass

        try:
            await my_robot.run()
        except asyncio.CancelledError:
            pass

    try:
        asyncio.run(_daemon_main())
    except Exception as e:
        print(f"Exception in child process: {e!r}")
        raise

@app.command(short_help="Start the robot process.")
def start():
    pidFile = Path('./run/robot.pid')
    pid = None

    if pidFile.is_file():
        pid = pidFile.read_text().strip()
    else:
        pidFile.parent.mkdir(parents=True, exist_ok=True)

        proc = multiprocessing.Process(target=_run_robot)
        proc.start()
        pidFile.write_text(str(proc.pid))


@app.command(short_help="Stop the robot process.")
def stop():
    pidFile = Path('./run/robot.pid')
    if not pidFile.is_file():
        print(":warning: No PID file found.")
        raise typer.Exit(code=1)

    try:
        pid = int(pidFile.read_text().strip())
    except ValueError:
        print(":warning: Invalid PID file.")
        pidFile.unlink(missing_ok=True)
        raise typer.Exit(code=1)

    try:
        try:
            os.killpg(pid, signal.SIGTERM)
            print(f"Stopped process group {pid}")
        except Exception:
            os.kill(pid, signal.SIGTERM)
            print(f"Stopped process {pid}")
    except ProcessLookupError:
        print(f":warning: Process {pid} not found.")

    pidFile.unlink(missing_ok=True)

@app.command(short_help="Take a screenshot and save it to path.")
def screenshot(path: str):
    print(":warning: Taking screenshot...")

if __name__ == "__main__":
    asyncio.run(app())