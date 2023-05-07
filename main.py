import os
import threading

threading.Thread(target=os.system, args=("python login.py",)).start()
threading.Thread(target=os.system, args=("python login3.py",)).start()


