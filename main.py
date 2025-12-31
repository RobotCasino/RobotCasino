import asyncio
import sys
import os
import signal
import datetime
from robot import Robot

PID_FILE = "robot.pid"

async def start_robot():
    if os.path.exists(PID_FILE):
        print(f"Error: {PID_FILE} exists. Is the robot already running?")
        return

    # Write PID file
    pid = os.getpid()
    with open(PID_FILE, "w") as f:
        f.write(str(pid))
    
    print(f"Robot started with PID {pid}")

    robot = Robot()
    
    shutdown_event = asyncio.Event()

    def handle_signal():
        shutdown_event.set()

    def handle_screenshot():
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        print(f"Taking screenshot: {filename}")
        asyncio.create_task(robot.screenshot(filename))

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGTERM, handle_signal)
    loop.add_signal_handler(signal.SIGINT, handle_signal)
    loop.add_signal_handler(signal.SIGUSR1, handle_screenshot)

    robot_task = asyncio.create_task(robot.run())

    try:
        await shutdown_event.wait()
    finally:
        robot_task.cancel()
        try:
            await robot_task
        except asyncio.CancelledError:
            pass
        
        await robot.close()
        
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

def close_robot():
    if not os.path.exists(PID_FILE):
        print("Error: Robot is not running (no PID file).")
        return

    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        
        os.kill(pid, signal.SIGTERM)
        print(f"Sent shutdown signal to PID {pid}")
    except FileNotFoundError:
        print("PID file not found.")
    except ProcessLookupError:
        print("Process not found. Cleaning up PID file.")
        os.remove(PID_FILE)
    except Exception as e:
        print(f"Error: {e}")

def take_screenshot():
    if not os.path.exists(PID_FILE):
        print("Error: Robot is not running (no PID file).")
        return

    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        
        os.kill(pid, signal.SIGUSR1)
        print(f"Sent screenshot signal to PID {pid}")
    except FileNotFoundError:
        print("PID file not found.")
    except ProcessLookupError:
        print("Process not found. Cleaning up PID file.")
        os.remove(PID_FILE)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "close":
            close_robot()
        elif sys.argv[1] == "screenshot":
            take_screenshot()
    else:
        asyncio.run(start_robot())