import pygetwindow
import time
from src.decorators.force_full_screen import forceFullScreenForThis

def maximizeMetamaskNotification():
    title = 'MetaMask Notification'
    time.sleep(7)
    windows = pygetwindow.getWindowsWithTitle(title)
    if len(windows) > 0:
        current_window = windows[0]
        current_window.activate()
        current_window.maximize()

def checkMetamaskNotification(fn):
    def exec(*args, **kwargs):
        maximizeMetamaskNotification()
        time.sleep(5)
        return fn(*args, **kwargs)
    return exec