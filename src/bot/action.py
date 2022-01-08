from random import random
from cv2 import cv2
import numpy as np
import pyautogui
import time

import pygetwindow

import src.bot.logger as Log
import src.env as env
from src.utils.number import addRandomness
from src.utils.image import printScreen, printScreenForWindow
from src.decorators.force_full_screen import forceFullScreenForThis
from src.utils.opencv import show

def moveToWithRandomness(x,y,t=env.mouse_move_speed):
    pos_x = x
    pos_y = y
    if env.window_object is not None and (not env.force_full_screen or not env.in_login_process):
        pos_x = pos_x+env.window_object.left
        pos_y = pos_y+env.window_object.top
    if env.cfg['is_retina_screen']:
        pos_x = pos_x / 2
        pos_y = pos_y / 2
    pyautogui.moveTo(addRandomness(pos_x,10),addRandomness(pos_y,10),t+random()/2)

def clickBtn(img,name=None, timeout=3, threshold = env.threshold['default']):
    Log.logger(None, progress_indicator=True)
    if not name is None:
        pass
    start = time.time()
    while(True):
        matches = getPositions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass
                return False
            continue
        if env.debug['clickBtn']:        
            show(matches, None, '[clickBtn] name -> {}'.format(name))
        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y)
        pyautogui.click()
        return True

def scroll():
    hero_item_list = getPositions(env.images['hero-item'], threshold = env.threshold['commom'])
    if env.debug['scroll']:        
        show(hero_item_list, None, '[scroll] hero_item_list')
    if (len(hero_item_list) == 0):
        return
    x,y,w,h = hero_item_list[len(hero_item_list)-1]
    moveToWithRandomness(x,y)

    if not env.cfg['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-env.cfg['scroll_size'])
    else:
        pyautogui.dragRel(0,-env.cfg['click_and_drag_amount'],duration=1, button='left')

def getPositions(target, threshold=env.threshold['default'],img = None):
    if img is None:
        running_multi_account = env.window_object is not None
        if running_multi_account and not env.force_full_screen:
            img = printScreenForWindow(env.window_object, env.in_login_process == False)
        else:
            img = printScreen()
        result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def goToHeroes():
    if clickBtn(env.images['go-back-arrow']):
        env.login_attempts = 0
    time.sleep(1)
    clickBtn(env.images['hero-icon'])
    time.sleep(1)

def goToGame():
    clickBtn(env.images['x'])
    clickBtn(env.images['x'])

    clickBtn(env.images['treasure-hunt-icon'])

def refreshHeroesPositions():
    Log.logger('🔃 Refreshing Heroes Positions')
    clickBtn(env.images['go-back-arrow'])
    clickBtn(env.images['treasure-hunt-icon'])
    clickBtn(env.images['treasure-hunt-icon'])

def activeWindow():
    try:
        env.window_object.activate()
    except:
        env.window_object.minimize()
        env.window_object.activate()

@forceFullScreenForThis
def goToNextMap():
    if clickBtn(env.images['new-map']):
        Log.logNewMapClicked()

def closeMetamaskWindow():
    try:
        title = 'MetaMask Notification'
        time.sleep(7)
        windows = pygetwindow.getWindowsWithTitle(title)
        for window in windows:
            window.close()
    except:
        print('error for close metamask window')

def maximizeMetamaskNotification():
    title = 'MetaMask Notification'
    time.sleep(8)
    windows = pygetwindow.getWindowsWithTitle(title)
    if len(windows) > 0:
        current_window = windows[0]
        current_window.activate()
        current_window.maximize()