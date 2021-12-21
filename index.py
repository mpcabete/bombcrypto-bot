# -*- coding: utf-8 -*-    
from cv2 import cv2

from captcha.solveCaptcha import solveCaptcha

from os import listdir
from src.logger import logger, loggerMapClicked
from random import random
from telebot import TeleBot
import numpy as np
import mss
import pyautogui
import time
import sys

import yaml


if __name__ == '__main__':
    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)

ct = c['threshold']
ch = c['home']

if not ch['enable']:
    print('>>---> Home feature not enabled\n')

pause = c['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = pause

pyautogui.FAILSAFE = False
hero_clicks = 0
telegram_notify = c['telegram']['notify']
login_attempts = 0
notify_count = 0
last_log_is_progress = False

if telegram_notify is True:
    if int(len(c['telegram']['bot_key'])) > 10 and int(len(c['telegram']['chat_id']) >= 5):
        bot = TeleBot(c['telegram']['bot_key'])
        telegram_chat_id = c['telegram']['chat_id']
        print('>>---> Telegram enabled.\n')
    else:
        print('>>---> Error setting telegram up. Notifications disabled. Check config.\n')
        telegram_notify = False
else:
    print('>>---> Telegram disabled.\n')




def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    # logger('{} with randomness -> {}'.format(int(n), randomized_n))
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2,pyautogui.easeOutQuad)


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

def loadHeroesToSendHome():
    file_names = listdir('./targets/heroes-to-send-home')
    heroes = []
    for file in file_names:
        path = './targets/heroes-to-send-home/' + file
        heroes.append(cv2.imread(path))

    print('>>---> %d heroes that should be sent home loaded' % len(heroes))
    return heroes

if ch['enable']:
    home_heroes = loadHeroesToSendHome()

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
full_stamina = cv2.imread('targets/full-stamina.png')

robot = cv2.imread('targets/robot.png')
# puzzle_img = cv2.imread('targets/puzzle.png')
# piece = cv2.imread('targets/piece.png')
slider = cv2.imread('targets/slider.png')



def show(rectangles, img = None):

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)





def clickBtn(img,name=None, timeout=3, threshold = ct['default']):
    logger(None, progress_indicator=True)
    if name is not None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    while(True):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if name is not None:
                    pass
                    # print('timed out')
                return False
            # print('button not found yet')
            continue

        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        # mudar moveto pra w randomness
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:,:,:3]


#### MINHAS ADIÇÕES

def checkScreen(button, confidence=ct['common']):
    try:
        object = pyautogui.locateOnScreen(button,confidence)
        result = pyautogui.center(object)
        return result
    except:
        return None

def matchPixel(x,y,color):
    matchScreen = pyautogui.screenshot()
    if matchScreen.getpixel((x, y)) == color:
        return True
    else:
        return False

def smartMove(image, confidence=ct['common'],justcheck=False,challenge=False):
    screenObj = checkScreen(image,confidence)
    if screenObj:
        if justcheck == True:
           return True
        else:
            pointx, pointy = screenObj
            pyautogui.moveTo(pointx, pointy,1,pyautogui.easeOutQuad)
            pyautogui.click()
            if challenge == True:
                return screenObj
            else:
                sys.stdout.write(f"\n Clicked on {image}\n")
                time.sleep(1)
                return True
    else:
        return None

def get_object_by_color(minx, maxx, miny, maxy, color, object="object"):
    telaChallenge = pyautogui.screenshot()
    objX = []
    objY = []
    try:
        for x in range(minx,maxx):
            for y in range(miny,maxy):
               if telaChallenge.getpixel((x, y)) == color:
                   objX.append(x)
                   objY.append(y)
        return objX, objY
    except:
        sys.stdout.write(f"\nError finding {object}\n")
        return False

## FIM DAS ADIÇÕES
def positions(target, threshold=ct['default'],img = None):
    if img is None:
        img = printSreen()
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

def scroll():

    commons = positions(images['commom-text'], threshold = ct['common'])
    if (len(commons) == 0):
        return
    x,y,w,h = commons[len(commons)-1]
#
    moveToWithRandomness(x,y,1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0,-c['click_and_drag_amount'],duration=1, button='left')


def clickButtons():
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(buttons)

def isHome(hero, buttons):
    y = hero[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            # if send-home button exists, the hero is not home
            return False
    return True

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

    green_bars = positions(images['green-bar'], threshold=ct['green_bar'])
    logger('🟩 %d green bars detected' % len(green_bars))
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    logger('🆗 %d buttons detected' % len(buttons))


    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('🆗 %d buttons with green bar detected' % len(not_working_green_bars))
        logger('👆 Clicking in %d heroes' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        moveToWithRandomness(x+offset+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        if hero_clicks > 20:
            logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)

def clickFullBarButtons():
    offset = 100
    full_bars = positions(images['full-stamina'], threshold=ct['default'])
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        logger('👆 Clicking in %d heroes' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        moveToWithRandomness(x+offset+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1

    return len(not_working_full_bars)

def goToHeroes():
    if clickBtn(images['go-back-arrow']):
        global login_attempts
        login_attempts = 0

    solveCaptcha(pause)
    #TODO tirar o sleep quando colocar o pulling
    time.sleep(1)
    clickBtn(images['hero-icon'])
    time.sleep(1)
    solveCaptcha(pause)

def goToGame():
    # in case of server overload popup
    clickBtn(images['x'])
    # time.sleep(3)
    clickBtn(images['x'])

    clickBtn(images['treasure-hunt-icon'])

def refreshHeroesPositions():

    logger('🔃 Refreshing Heroes Positions')
    clickBtn(images['go-back-arrow'])
    clickBtn(images['treasure-hunt-icon'])

    # time.sleep(3)
    clickBtn(images['treasure-hunt-icon'])

def login():
    global login_attempts
    logger('😿 Checking if game has disconnected')

    if login_attempts > 3:
        logger('🔃 Too many login attempts, refreshing')
        login_attempts = 0
        pyautogui.hotkey('ctrl','f5')
        time.sleep(4)
        return False

    connectWalletBtnScreen = checkScreen(images['connect-wallet'], confidence=ct['connect_Wallet_button'])
    if connectWalletBtnScreen:
        try:
            login_attempts = login_attempts + 1
            time.sleep(1)
            walletx, wallety = connectWalletBtnScreen
            pyautogui.moveTo(walletx, wallety, 1, pyautogui.easeOutQuad)
            pyautogui.click()
            logger('Connect wallet button pressed')
            solveCaptcha(pause)
        except:
            logger('Error clicking on wallet button')
            login_attempts = 4  # Probla
            return False

    if clickBtn(images['metamask_pending'], name='metamask_pending_button', timeout = 2, threshold = 1):
        logger('Metamask peding login found')
        try:
            clickBtn(images['metamask_cancel'], name='metamask_cancel_button', timeout = 2)
            clickBtn(images['bombcrypto_logo'], name='bombcrypto_blank_area', timeout = 2)
            pyautogui.hotkey('ctrl','f5')
            time.wait(4)
            return False
        except:
            login_attempts = login_attempts + 1

    elif not clickBtn(images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
        if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', threshold  = ct['select_wallet_buttons'] ):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)

    if clickBtn(images['select-wallet-2'], name='sign button', timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout = 15):
            logger('Successfully Logged, treasure button found')
            login_attempts = 0
            return True
        # click ok button

    if clickBtn(images['ok'], name='okBtn', timeout=5):
        logger('OK Button Clicked')
        return False

    login_attempts += 1



def sendHeroesHome():
    if not ch['enable']:
        return
    heroes_positions = []
    for hero in home_heroes:
        hero_positions = positions(hero, threshold=ch['hero_threshold'])
        if not len (hero_positions) == 0:
            #TODO maybe pick up match with most wheight instead of first
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)
    # if send-home button exists, the hero is not home
    go_home_buttons = positions(images['send-home'], threshold=ch['home_button_threshold'])
    # TODO pass it as an argument for both this and the other function that uses it
    go_work_buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    for position in heroes_positions:
        if not isHome(position,go_home_buttons):
            print(isWorking(position, go_work_buttons))
            if(not isWorking(position, go_work_buttons)):
                print ('hero not working, sending him home')
                moveToWithRandomness(go_home_buttons[0][0]+go_home_buttons[0][2]/2,position[1]+position[3]/2,1)
                pyautogui.click()
            else:
                print ('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')





def refreshHeroes():
    logger('🏢 Search for heroes to work')

    goToHeroes()

    if c['select_heroes_mode'] == "full":
        logger('⚒️ Sending heroes with full stamina bar to work', 'green')
    elif c['select_heroes_mode'] == "green":
        logger('⚒️ Sending heroes with green stamina bar to work', 'green')
    else:
        logger('⚒️ Sending all heroes to work', 'green')

    buttonsClicked = 1
    empty_scrolls_attempts = c['scroll_attemps']

    while(empty_scrolls_attempts >0):
        if c['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons()
        elif c['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked = clickButtons()

        sendHeroesHome()

        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        time.sleep(2)
    logger('💪 {} heroes sent to work'.format(hero_clicks))
    goToGame()

def checkConnection():
    global notify_count
    expandScrx, expandScry = 0, 0
    walletSelectionScreen = checkScreen(images['select-wallet-1-hover'],confidence=ct['select_wallet_buttons'])
    connectWalletBtnScreen = checkScreen(images['connect-wallet'],confidence=ct['connect_Wallet_button'])
    treasureBtnScreen = checkScreen(images['treasure-hunt-icon'])
    okBtnScreen = checkScreen(images['ok'])
    expandScrx, expandScry = get_object_by_color(700,1660,400,1000,(64,173,211), "expand")
    if okBtnScreen:
        logger('Pressing Ok')
        clickBtn(images['ok'], name='okBtn', timeout=5)
        time.sleep(15)
        connected = login()
        return connected
    elif treasureBtnScreen:
        logger('Treasure button found!')
        return True
    elif walletSelectionScreen:
        logger('Wallet selection screen found, refreshing!')
        pyautogui.hotkey('ctrl','f5')
        time.sleep(5)
        return False
    elif connectWalletBtnScreen:
        logger('Connect wallet button detected, logging in!')
        connected = login()
        return connected
    elif len(expandScrx) < 500 and len(expandScry) < 500:
        #Check if the screen is visible
        notify_count += 1
        logger('Window not found')
        if notify_count > c['telegram']['error_count'] and telegram_notify is True:
            logger("Sending telegram message.")
            bot.send_message(telegram_chat_id,"Tela do Cryptobomb não encontrada. Verificar navegador.",disable_notification=True)
            notify_count = 0
        logger('Waiting 60 seconds to try again')
        #50 aqui + 10 da função de conexão
        time.sleep(50)
        return False
    else:
        logger('Game seems to be running fine.')
        notify = 0
        return True


def main():
    time.sleep(5)
    t = c['time_intervals']

    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    "check_for_captcha" : 0,
    "refresh_heroes" : 0
    }

    while True:
        now = time.time()
        sys.stdout.flush()
        connected = checkConnection()
        if connected:
            logger(f"""Connected - {time.strftime("%H:%M:%S")}""")
            last["login"] = now
        while not connected:
            logger("Game is not running.")
            sys.stdout.flush()
            connected = checkConnection()
            last["login"] = now
            if connected:
                logger('Connected successfully.')
            else:
                logger("Couldn't connect. Trying again in 10 seconds.")
                time.sleep(10)
        while connected:
            now = time.time()

            if now - last["login"] > addRandomness(t['check_for_login'] * 60):
                sys.stdout.flush()
                connected = checkConnection()

            if now - last["check_for_captcha"] > addRandomness(t['check_for_captcha'] * 60):
                last["check_for_captcha"] = now
                solveCaptcha(pause)

            if now - last["heroes"] > addRandomness(t['send_heroes_for_work'] * 60):
                last["heroes"] = now
                refreshHeroes()

            if now - last["new_map"] > t['check_for_new_map_button']:
                last["new_map"] = now

                if clickBtn(images['new-map']):
                    loggerMapClicked()

            if now - last["refresh_heroes"] > addRandomness( t['refresh_heroes_positions'] * 60):
                solveCaptcha(pause)
                last["refresh_heroes"] = now
                refreshHeroesPositions()

            logger(None, progress_indicator=True)
            sys.stdout.flush()
            time.sleep(1)
        time.sleep(1)

main()


#cv2.imshow('img',sct_img)
#cv2.waitKey()

# colocar o botao em pt
# soh resetar posiçoes se n tiver clickado em newmap em x segundos


