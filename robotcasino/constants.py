import pathlib

SOCKET_PATH = pathlib.Path(pathlib.Path.home() / ".robotcasino.socket")
PID_PATH =  pathlib.Path("/tmp/robotcasino.pid")

__ALL__ = ["PID_PATH", "SOCKET_PATH"]