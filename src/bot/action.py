from random import random
from cv2 import cv2
import numpy as np
import pyautogui
import time

from src.logger import logger
import src.env as env
from src.utils.number import addRandomness
from src.utils.image import printScreen, printScreenForWindow

def moveToWithRandomness(x,y,t):
    pos_x = x
    pos_y = y
    if env.window_object is not None:
        pos_x = pos_x+env.window_object.left
        pos_y = pos_y+env.window_object.top
    pyautogui.moveTo(addRandomness(pos_x,10),addRandomness(pos_y,10),t+random()/2)

def clickBtn(img,name=None, timeout=3, threshold = env.threshold['default']):
    logger(None, progress_indicator=True)
    if not name is None:
        pass
    start = time.time()
    while(True):
        matches = get_positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass
                return False
            continue
        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True

def scroll():
    commoms = get_positions(env.images['hero-item'], threshold = env.threshold['commom'])
    if (len(commoms) == 0):
        return
    x,y,w,h = commoms[len(commoms)-1]
    moveToWithRandomness(x,y,1)

    if not env.cfg['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-env.cfg['scroll_size'])
    else:
        pyautogui.dragRel(0,-env.cfg['click_and_drag_amount'],duration=1, button='left')

def get_positions(target, threshold=env.threshold['default'],img = None):
    if img is None:
        if env.window_object is not None:
            img = printScreenForWindow(env.window_object)
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
    logger('🔃 Refreshing Heroes Positions')
    clickBtn(env.images['go-back-arrow'])
    clickBtn(env.images['treasure-hunt-icon'])
    clickBtn(env.images['treasure-hunt-icon'])

def active_window():
    try:
        env.window_object.activate()
    except:
        env.window_object.activate()
