from pathlib import Path
import sys
import threading
from time import sleep

from backend import backend
from frontend import frontend


running_flag = Path("running.flg")
exit_flag = Path("exit.flg")

if exit_flag.is_file():
    exit_flag.unlink()

if not running_flag.is_file():
    running_flag.touch()
else:
    print("Already running")
    sys.exit(-1)

threading.Thread(target=backend.main, daemon=True).start()
threading.Thread(target=frontend.main, daemon=True).start()

while not exit_flag.is_file():
    sleep(1)

if running_flag.is_file():
    running_flag.unlink()
