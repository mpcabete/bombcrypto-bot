from cv2 import cv2
import numpy as np
import mss
import pyautogui
import time

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True
hero_clicks = 0
login_attempts = 0


btn = cv2.imread('go-work-btn.png')
commom = cv2.imread('text.png')
arrow = cv2.imread('arrow.png')
hero = cv2.imread('hero.png')
xbtn = cv2.imread('x.png')
teasureHunt = cv2.imread('hunt.png')

okBtn = cv2.imread('ok.png')
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

def positions(target, trashhold=.70):
    img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= trashhold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll():
    commoms = positions(commom, trashhold = .60)
    if (len(commoms) == 0):
        print('no commom text found')
        return
    x,y,w,h = commoms[len(commoms)-1]
    print('moving to {},{}'.format(x,y))

    pyautogui.moveTo(x,y)
    pyautogui.dragRel(0,-500,duration=1)

def clickButtons(trashhold=.95):
    buttons = positions(btn, trashhold)
    print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        pyautogui.click(x+(w/2),y+(h/2))
        global hero_clicks
        hero_clicks = hero_clicks + 1
        print('{} heroes sent to work so far'.format(hero_clicks))
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(buttons)

def goToHeroes():
    if clickBtn(arrow):
        global login_attempts
        login_attempts = 0

    time.sleep(5)
    clickBtn(hero)

def goToGame():
    clickBtn(xbtn)

    clickBtn(teasureHunt)

def login():
    global login_attempts

    if login_attempts > 3:
        print('too many login attempts, refreshing')
        login_attempts = 0
        pyautogui.press('f5')
        return

    if clickBtn(okBtn):
        time.sleep(15)
        print('ok button clicked')

    if clickBtn(connectWalletBtn):
        #TODO mto ele da erro e poco o botao n abre
        time.sleep(10)

    if clickBtn(signBtn):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        print('sign button clicked')
        print('{} login attempt'.format(login_attempts))
        time.sleep(5)
        if clickBtn(teasureHunt):
            print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        time.sleep(15)
        return
        # click ok button

    if not clickBtn(selectMetamaskBtn):
        if clickBtn(selectMetamaskHoverBtn):
            time.sleep(20)
    else:
        time.sleep(20)

    if clickBtn(signBtn):
        login_attempts = login_attempts + 1
        print('sign button clicked')
        print('{} login attempt'.format(login_attempts))
        time.sleep(25)
        if clickBtn(teasureHunt):
            print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        time.sleep(15)
        # click ok button




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

        if now - last["login"] > 120:
            last["login"] = now
            #print('checking for login')
            login()

        if now - last["heroes"] > 60 * 30:
            last["heroes"] = now
            print('sending heroes to work')
            refreshHeroes()

        if now - last["new_map"] > 60:
            last["new_map"] = now
            #print('checking for New Map Button')
            if clickBtn(newMapBtn):
                print('new map button clicked')

        #clickBtn(teasureHunt)
        time.sleep(1)

main()





#cv2.imshow('img',sct_img)
#cv2.waitKey()
# aumentar tempo antes do sign
# chacar se tem o sign antes de aperta o connect wallet
# arrumar aquela parte do codigo copiado onde tem q checar o sign 2 vezes
# colocar o botao em pt
# dar uma olhada no bug de quando uma janela do metamask pra assinar fica aberto, e ver como o programa reage
# se esperar mto pra assinar ele n vai
# melhorar o log
