from cv2 import cv2
import numpy as np
import mss
import pyautogui
import time

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


btn = cv2.imread('go-work-btn.png')
commom = cv2.imread('text.png')
arrow = cv2.imread('arrow.png')
hero = cv2.imread('hero.png')
xbtn = cv2.imread('x.png')
teasureHunt = cv2.imread('hunt.png')

connectWalletBtn = cv2.imread('wallet.png')
selectMetamaskHoverBtn = cv2.imread('wallet1.png')
selectMetamaskBtn = cv2.imread('wallet1-1.png')
signBtn = cv2.imread('wallet2.png')



def printSreen():
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        #sct_img = np.array(sct.grab(monitor))
        sct_img = np.array(sct.grab(sct.monitors[0]))
        return sct_img[:,:,:3]

def positions(target):
    img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= .60)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll():
    commoms = positions(commom)
    x,y,w,h = commoms[len(commoms)-1]

    pyautogui.moveTo(x,y)
    pyautogui.dragRel(0,-500,duration=1)

def clickButtons():
    buttons = positions(btn)
    for (x, y, w, h) in buttons:
        pyautogui.click(x+(w/2),y+(h/2))
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(buttons)

def goToHeroes():
    x,y,w,h = positions(arrow)[0]
    pyautogui.click(x+w/2,y+h/2)

    x,y,w,h = positions(hero)[0]
    pyautogui.click(x+w/2,y+h/2)

def goToGame():
    x,y,w,h = positions(xbtn)[0]
    pyautogui.click(x+w/2,y+h/2)

    x,y,w,h = positions(teasureHunt)[0]
    pyautogui.click(x+w/2,y+h/2)

def login():
    x,y,w,h = positions(connectWalletBtn)[0]
    pyautogui.click(x+w/2,y+h/2)
    time.sleep(5)

    try:
        x,y,w,h = positions(selectMetamaskBtn)[0]
        pyautogui.click(x+w/2,y+h/2)
        time.sleep(5)
    except:
        print('metamask hover detected')
        x,y,w,h = positions(selectMetamaskHoverBtn)[0]
        pyautogui.click(x+w/2,y+h/2)
        time.sleep(5)


    x,y,w,h = positions(signBtn)[0]
    pyautogui.click(x+w/2,y+h/2)

login()

def main():
    goToHeroes()
    buttonsClicked = 1
    while(buttonsClicked >0):
        scroll()
        time.sleep(2)
        buttonsClicked = clickButtons()
        print(buttonsClicked)
    goToGame()

#while(True):
    #main()
    #time.sleep(60*5)



#cv2.imshow('img',sct_img)
#cv2.waitKey()

