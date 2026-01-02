import asyncio
import multiprocessing
import os

async def say_after(delay: int, what: str):
    await asyncio.sleep(delay)
    print(what)

async def _child_main():
    await say_after(5, "I'm the child process")

def _run_child():
    os.setsid()

    asyncio.run(_child_main())
    os._exit(0)

async def main():
    try:
        pid = os.fork()
    except AttributeError:
        proc = multiprocessing.Process(target=_run_child)
        proc.start()
        return

   
    if pid == 0:

        return

   

if __name__ == "__main__":
    asyncio.run(main())