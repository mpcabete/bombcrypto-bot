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
newMapBtn = cv2.imread('new-map.png')


def clickBtn(img):
    matches = positions(img)
    if(len(matches)==0):
        return False
    x,y,w,h = matches[0]
    pyautogui.moveTo(x+w/2,y+h/2,1)
    pyautogui.click()
    return True

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

    yloc, xloc = np.where(result >= .70)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll():
    commoms = positions(commom)
    if (len(commoms) == 0):
        return
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
    clickBtn(arrow)

    clickBtn(hero)

def goToGame():
    clickBtn(xbtn)

    clickBtn(teasureHunt)

def login():
    if clickBtn(connectWalletBtn):
        time.sleep(5)

    if not clickBtn(selectMetamaskBtn):
        if clickBtn(selectMetamaskHoverBtn):
            time.sleep(5)
    else:
        time.sleep(5)

    if clickBtn(signBtn):
        time.sleep(15)
        print('sl')




def refreshHeroes():
    goToHeroes()
    buttonsClicked = 1
    while(buttonsClicked >0):
        scroll()
        time.sleep(2)
        buttonsClicked = clickButtons()
    goToGame()

def main():
    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    }

    while True:
        now = time.time()

        if now - last["login"] > 100:
            last["login"] = now
            print('checking for login')
            login()

        if now - last["heroes"] > 300:
            last["heroes"] = now
            print('sending heroes to work')
            refreshHeroes()

        if now - last["new_map"] > 30:
            last["new_map"] = now
            print('checking for New Map Button')
            clickBtn(newMapBtn)

        #clickBtn(teasureHunt)
        time.sleep(1)

main()





#cv2.imshow('img',sct_img)
#cv2.waitKey()
# aumentar tempo antes do sign
# chacar se tem o sign antes de aperta o connect wallet
# melhorar o log
