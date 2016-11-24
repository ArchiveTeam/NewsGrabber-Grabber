import os
import time

open('UPDATE', 'w').close()

while True:
    if os.path.isfile('UPDATE'):
        time.sleep(60)
        os.system('git pull')
        os.system('python start.py')