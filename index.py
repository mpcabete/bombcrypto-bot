from cv2 import cv2
import numpy as np
import mss
import pyautogui
import time

import yaml
if __name__ == '__main__':

    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)
ct = c['trashhold']

pyautogui.PAUSE = c['time_intervals']['interval_between_moviments']

pyautogui.FAILSAFE = True
hero_clicks = 0
login_attempts = 0







go_work_img = cv2.imread('targets/go-work.png')
commom_img = cv2.imread('targets/commom-text.png')
arrow_img = cv2.imread('targets/go-back-arrow.png')
hero_img = cv2.imread('targets/hero-icon.png')
x_button_img = cv2.imread('targets/x.png')
teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
ok_btn_img = cv2.imread('targets/ok.png')
connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
select_wallet_hover_img = cv2.imread('targets/select-wallet-1-hover.png')
select_metamask_no_hover_img = cv2.imread('targets/select-wallet-1-no-hover.png')
sign_btn_img = cv2.imread('targets/select-wallet-2.png')
new_map_btn_img = cv2.imread('targets/new-map.png')


def clickBtn(img,name=None, timeout=3, trashhold = ct['default']):
    if not name is None:
        print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    clicked = False
    while(not clicked):
        matches = positions(img, trashhold=trashhold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    print('timed out')
                return False
            # print('button not found yet')
            continue

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

def positions(target, trashhold=ct['default']):
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

    commoms = positions(commom_img, trashhold = ct['commom'])
    if (len(commoms) == 0):
        print('no commom text found')
        return
    x,y,w,h = commoms[len(commoms)-1]
    print('moving to {},{} and scrolling'.format(x,y))
#
    pyautogui.moveTo(x,y,1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0,-500,duration=1)
        print(c['use_click_and_drag_instead_of_scroll'])


def clickButtons():
    buttons = positions(go_work_img, trashhold=ct['go_to_work_btn'])
    print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        pyautogui.moveTo(x+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        print('{} heroes sent to work so far'.format(hero_clicks))
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(buttons)

def goToHeroes():
    if clickBtn(arrow_img):
        global login_attempts
        login_attempts = 0

    # time.sleep(5)
    clickBtn(hero_img)
    # time.sleep(5)

def goToGame():
    # in case of server overload popup
    clickBtn(x_button_img)
    # time.sleep(3)
    clickBtn(x_button_img)

    clickBtn(teasureHunt_icon_img)

def refreshHeroesPositions():
    clickBtn(arrow_img)
    clickBtn(teasureHunt_icon_img)
    # time.sleep(3)
    clickBtn(teasureHunt_icon_img)

def login():
    global login_attempts

    if login_attempts > 3:
        print('too many login attempts, refreshing')
        login_attempts = 0
        pyautogui.press('f5')
        return

    if clickBtn(connect_wallet_btn_img, name='connectWalletBtn', timeout = 10):
        print('connect wallet button clicked')
        #TODO mto ele da erro e poco o botao n abre
        # time.sleep(10)

    if clickBtn(sign_btn_img, name='sign button', timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        print('sign button clicked')
        print('{} login attempt'.format(login_attempts))
        # time.sleep(5)
        if clickBtn(teasureHunt_icon_img, name='teasureHunt', timeout = 15):
            print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)
        return
        # click ok button

    if not clickBtn(select_metamask_no_hover_img, name='selectMetamaskBtn'):
        if clickBtn(select_wallet_hover_img, name='selectMetamaskHoverBtn', trashhold = ct['select_wallet_buttons'] ):
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo 
            print('sleep in case there is no metamask text removed')
            # time.sleep(20)
    else:
        print('sleep in case there is no metamask text removed')
        # time.sleep(20)

    if clickBtn(sign_btn_img, name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1
        print('sign button clicked')
        print('{} login attempt'.format(login_attempts))
        # time.sleep(25)
        if clickBtn(teasureHunt_icon_img, name='teasureHunt', timeout=25):
            print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)

    if clickBtn(ok_btn_img, name='okBtn', timeout=5):
        # time.sleep(15)
        print('ok button clicked')




def refreshHeroes():
    goToHeroes()
    buttonsClicked = 1
    while(buttonsClicked >0):
        scroll()
        time.sleep(2)
        buttonsClicked = clickButtons()
    goToGame()

def main():
    print()
    print('\nPlease, consider buying me a coffe 😊:')
    print('0xbd06182D8360FB7AC1B05e871e56c76372510dDf\n')
    time.sleep(5)
    t = c['time_intervals']

    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    "refresh_heroes" : 0
    }

    while True:
        now = time.time()

        if now - last["login"] > t['check_for_login'] * 60:
            last["login"] = now
            #print('checking for login')
            login()

        if now - last["heroes"] > t['send_heroes_for_work'] * 60:
            last["heroes"] = now
            print('sending heroes to work')
            refreshHeroes()

        if now - last["new_map"] > t['check_for_new_map_button']:
            last["new_map"] = now
            #print('checking for New Map Button')
            if clickBtn(new_map_btn_img):
                print('new map button clicked')

        if now - last["refresh_heroes"] > t['refresh_heroes_positions'] * 60 :
            last["refresh_heroes"] = now
            refreshHeroesPositions()
            print('Refreshing Heroes Positions')

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
# add argumets
# salvar timestamp dos clickes em newmap em um arquivo
# soh resetar posiçoes se n tiver clickado em newmap em x segundos
