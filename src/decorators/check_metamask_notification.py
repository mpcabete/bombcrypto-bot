import time
from src.bot.action import maximizeMetamaskNotification

def checkMetamaskNotification(fn):
    def exec(*args, **kwargs):
        maximizeMetamaskNotification()
        time.sleep(5)
        return fn(*args, **kwargs)
    return exec