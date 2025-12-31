import os
from signal import signal, SIGTERM
import sys
from types import FrameType

class Process:

    __pid_file = "robot.pid"

    def __check(self) -> bool:
        return True

    def __create_pid_file(self) -> None:
        with open(self.__pid_file, "w") as f:
            f.write(str(os.getpid()))

    def __handle_shutdown(self, sig: int, frame: FrameType | None) -> None:
        pass


    def startListening(self):
        if not self.__check():
            print("Another instance is already running.", file=sys.stderr)
            sys.exit(1)
        
        self.__create_pid_file()

        signal(SIGTERM, self.__handle_shutdown)
        
        
