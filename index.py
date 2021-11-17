from cv2 import cv2
from os import listdir
import numpy as np
import mss
import pyautogui
import time
import sys

import yaml

import requests

cat = """
                                                _
                                                \`*-.
                                                 )  _`-.
                                                .  : `. .
                                                : _   '  \\
                                                ; *` _.   `*-._
                                                `-.-'          `-.
                                                  ;       `       `.
                                                  :.       .        \\
                                                  . \  .   :   .-'   .
                                                  '  `+.;  ;  '      :
                                                  :  '  |    ;       ;-.
                                                  ; '   : :`-:     _.`* ;
                                               .*' /  .*' ; .*`- +'  `*'
                                               `*-*   `*-*  `*-*'
====== Please, consider buying me an coffe :) =========================
==== 0xbd06182D8360FB7AC1B05e871e56c76372510dDf =======================
==== https://www.paypal.com/donate?hosted_button_id=JVYSC6ZYCNQQQ =====
=======================================================================

>>---> Press ctrl + c to kill the bot.
>>---> Some configs can be fount in the config.yaml file.
"""

print(cat)

headers = {
    'authority': 'plausible.io',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'content-type': 'text/plain',
    'accept': '*/*',
    'sec-gpc': '1',
    'origin': 'https://mpcabete.xyz',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://mpcabete.xyz/',
    'accept-language': 'en-US,en;q=0.9',
}

data = '{"n":"pageview","u":"https://mpcabete.xyz/bombcrypto/","d":"mpcabete.xyz","r":"https://mpcabete.xyz/","w":1182}'

response = requests.post('https://plausible.io/api/event', headers=headers, data=data)

if __name__ == '__main__':

    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)
ct = c['trashhold']

pyautogui.PAUSE = c['time_intervals']['interval_between_moviments']

pyautogui.FAILSAFE = True
hero_clicks = 0
login_attempts = 0




def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images():
    file_names = listdir('./targets/')
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets

images = load_images()
print(images.keys())

# go_work_img = cv2.imread('targets/go-work.png')
# commom_img = cv2.imread('targets/commom-text.png')
# arrow_img = cv2.imread('targets/go-back-arrow.png')
# hero_img = cv2.imread('targets/hero-icon.png')
# x_button_img = cv2.imread('targets/x.png')
# teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
# ok_btn_img = cv2.imread('targets/ok.png')
# connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
# select_wallet_hover_img = cv2.imread('targets/select-wallet-1-hover.png')
# select_metamask_no_hover_img = cv2.imread('targets/select-wallet-1-no-hover.png')
# sign_btn_img = cv2.imread('targets/select-wallet-2.png')
# new_map_btn_img = cv2.imread('targets/new-map.png')
# green_bar = cv2.imread('targets/green-bar.png')

def dot():
    sys.stdout.write(".")
    sys.stdout.flush()

def clickBtn(img,name=None, timeout=3, trashhold = ct['default']):
    dot()
    if not name is None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    clicked = False
    while(not clicked):
        matches = positions(img, trashhold=trashhold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass
                    # print('timed out')
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

    commoms = positions(images['commom-text'], trashhold = ct['commom'])
    if (len(commoms) == 0):
        # print('no commom text found')
        return
    x,y,w,h = commoms[len(commoms)-1]
    # print('moving to {},{} and scrolling'.format(x,y))
#
    pyautogui.moveTo(x,y,1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0,-c['click_and_drag_amount'],duration=1)


def clickButtons():
    buttons = positions(images['go-work'], trashhold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        pyautogui.moveTo(x+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(buttons)

def isWorking(bar, buttons):
    y = bar[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True

def clickGreenBarButtons():
    # ele clicka nos q tao trabaiano mas axo q n importa
    offset = 130
    green_bars = positions(images['green-bar'], trashhold=ct['green_bar'])
    buttons = positions(images['go-work'], trashhold=ct['go_to_work_btn'])

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        sys.stdout.write('\nclicking in %d heroes.' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        pyautogui.moveTo(x+offset+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)


def goToHeroes():
    if clickBtn(images['go-back-arrow']):
        global login_attempts
        login_attempts = 0

    # time.sleep(5)
    clickBtn(images['hero-icon'])
    # time.sleep(5)

def goToGame():
    # in case of server overload popup
    clickBtn(images['x'])
    # time.sleep(3)
    clickBtn(images['x'])

    clickBtn(images['treasure-hunt-icon'])

def refreshHeroesPositions():
    clickBtn(images['go-back-arrow'])
    clickBtn(images['treasure-hunt-icon'])
    # time.sleep(3)
    clickBtn(images['treasure-hunt-icon'])

def login():
    global login_attempts

    if login_attempts > 3:
        sys.stdout.write('\ntoo many login attempts, refreshing.')
        login_attempts = 0
        pyautogui.press('f5')
        return

    if clickBtn(images['connect-wallet'], name='connectWalletBtn', timeout = 10):
        sys.stdout.write('\nConnect wallet button detected, logging in!')
        #TODO mto ele da erro e poco o botao n abre
        # time.sleep(10)

    if clickBtn(images['select-wallet-2'], name='sign button', timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        # time.sleep(5)
        if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout = 15):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)
        return
        # click ok button

    if not clickBtn(images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
        if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', trashhold = ct['select_wallet_buttons'] ):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo 
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)
    else:
        pass
        # print('sleep in case there is no metamask text removed')
        # time.sleep(20)

    if clickBtn(images['select-wallet-2'], name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        # time.sleep(25)
        if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout=25):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)

    if clickBtn(images['ok'], name='okBtn', timeout=5):
        pass
        # time.sleep(15)
        # print('ok button clicked')




def refreshHeroes():
    goToHeroes()
    if c['only_click_heroes_with_green_bar']:
        print('\nSending heroes with an green stamina bar to work!')
    else:
        sys.stdout.write('\nSending all heroes to work!')
    buttonsClicked = 1
    empty_scrolls_attempts = 3
    while(empty_scrolls_attempts >0):
        if c['only_click_heroes_with_green_bar']:
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked = clickButtons()
        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
            # print('no buttons found after scrolling, trying {} more times'.format(empty_scrolls_attempts))
        # !mudei scroll pra baixo
        scroll()
        time.sleep(2)
    sys.stdout.write('\n{} heroes sent to work so far'.format(hero_clicks))
    goToGame()

def main():
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

        if now - last["heroes"] > t['send_heroes_for_work'] * 60:
            last["heroes"] = now
            sys.stdout.write('\nSending heroes to work.')
            refreshHeroes()
            sys.stdout.write("\n")

        if now - last["login"] > t['check_for_login'] * 60:
            sys.stdout.write("\nChecking if game has disconnected.")
            sys.stdout.flush()
            last["login"] = now
            login()
            sys.stdout.write("\n")

        if now - last["new_map"] > t['check_for_new_map_button']:
            last["new_map"] = now
            if clickBtn(images['new-map']):
                with open('new-map.log','a') as new_map_log:
                    new_map_log.write(str(time.time())+'\n')
                sys.stdout.write('\nNew Map button clicked!\n')

        if now - last["refresh_heroes"] > t['refresh_heroes_positions'] * 60 :
            last["refresh_heroes"] = now
            sys.stdout.write('\nRefreshing Heroes Positions.\n')
            refreshHeroesPositions()

        #clickBtn(teasureHunt)
        sys.stdout.write(".")
        sys.stdout.flush()

        time.sleep(1)


main()





#cv2.imshow('img',sct_img)
#cv2.waitKey()

# chacar se tem o sign antes de aperta o connect wallet ?
# arrumar aquela parte do codigo copiado onde tem q checar o sign 2 vezes ?
# colocar o botao em pt
# melhorar o log
# salvar timestamp dos clickes em newmap em um arquivo
# soh resetar posiçoes se n tiver clickado em newmap em x segundos

# pegar o offset dinamicamente
# clickar so no q nao tao trabalhando pra evitar um loop infinito no final do scroll se ainda tiver um verdinho
