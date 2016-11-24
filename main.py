import os
import time

while True:
    if os.path.isfile('UPDATE'):
        time.sleep(60)
        os.system('git pull')
        os.system('python start.py')