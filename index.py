# -*- coding: utf-8 -*-
from cv2 import cv2
from datetime import datetime
from os import listdir
from src.logger import logger, loggerMapClicked
from random import randint
from random import random
import pygetwindow
import numpy as np
import mss
import pyautogui
import time
import sys

import yaml

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
=========================================================================
========== 💰 Have I helped you in any way? All I ask is a tip! 🧾 ======
========== ✨ Faça sua boa ação de hoje, manda aquela gorjeta! 😊 =======
=========================================================================
======================== vvv BCOIN BUSD BNB vvv =========================
============== 0xbd06182D8360FB7AC1B05e871e56c76372510dDf ===============
=========================================================================
===== https://www.paypal.com/donate?hosted_button_id=JVYSC6ZYCNQQQ ======
=========================================================================
>>---> Press ctrl + c to kill the bot.
>>---> Some configs can be found in the config.yaml file."""

print(cat)
time.sleep(2)

if __name__ == '__main__':
    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)

ct = c['threshold']
ch = c['home']

if not ch['enable']:
    print('House is not enable')
print('\n')

pause = c['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = pause

pyautogui.FAILSAFE = False
hero_clicks = 0
login_attempts = 0
last_log_is_progress = False


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


def moveToWithRandomness(x, y, t):
    pyautogui.moveTo(addRandomness(x, 10), addRandomness(y, 10), t + random() / 2)


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

full_stamina = cv2.imread('targets/full-stamina.png')

robot = cv2.imread('targets/robot.png')


def show(rectangles, img=None):
    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255, 255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)


def check_login(img, name=None, timeout=3, threshold=ct['default']):
    logger(None, progress_indicator=True)
    if not name is None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    while True:
        matches = positions(img, threshold=threshold)
        if len(matches) == 0:
            hast_timed_out = time.time() - start > timeout
            if hast_timed_out:
                if not name is None:
                    pass
                    # print('timed out')
                return False
            # print('button not found yet')
            continue

        x, y, w, h = matches[0]
        pos_click_x = x + w / 2
        pos_click_y = y + h / 2
        # mudar moveto pra w randomness
        return True
        # print("THIS SHOULD NOT PRINT")


def clickBtn(img, name=None, timeout=3, threshold=ct['default']):
    logger(None, progress_indicator=True)
    if not name is None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    while True:
        matches = positions(img, threshold=threshold)
        if len(matches) == 0:
            hast_timed_out = time.time() - start > timeout
            if hast_timed_out:
                if not name is None:
                    pass
                    # print('timed out')
                return False
            # print('button not found yet')
            continue

        x, y, w, h = matches[0]
        pos_click_x = x + w / 2
        pos_click_y = y + h / 2
        # mudar moveto pra w randomness
        moveToWithRandomness(pos_click_x, pos_click_y, 1)
        pyautogui.click()
        return True
        # print("THIS SHOULD NOT PRINT")


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:, :, :3]


def positions(target, threshold=ct['default'], img=None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
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
    commoms = positions(images['commom-text'], threshold=ct['commom'])
    if (len(commoms) == 0):
        return
    x, y, w, h = commoms[len(commoms) - 1]
    #
    moveToWithRandomness(x, y, 1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0, -c['click_and_drag_amount'], duration=1, button='left')


def clickButtons():
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(buttons)


def isHome(hero, buttons):
    y = hero[1]

    for (_, button_y, _, button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            # if send-home button exists, the hero is not home
            return False
    return True


def isWorking(bar, buttons):
    y = bar[1]

    for (_, button_y, _, button_h) in buttons:
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
        moveToWithRandomness(x + offset + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks += 1
        if hero_clicks > 20:
            logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
        # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
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
        moveToWithRandomness(x + offset + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks += 1

    return len(not_working_full_bars)


def goToHeroes():
    if clickBtn(images['go-back-arrow']):
        global login_attempts
        login_attempts = 0
    clickBtn(images['hero-icon'])


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
    # TODO melhorar o login, alternar entre metamask tab para corrigir o erro de nao logar com ele minimizado
    #
    global login_attempts
    logger('😿 Wallet button found, processing login again.')
    if login_attempts > 0:
        logger(f'Loggins attempts: {login_attempts}. Bot will refresh page after 2 attempts.')

    if login_attempts > 1:
        logger('🔃 Too many login attempts, refreshing')
        login_attempts = 0
        pyautogui.hotkey('ctrl', 'f5')
        return

    if clickBtn(images['connect-wallet'], name='connectWalletBtn', timeout=10):
        logger('🎉 Connect wallet button detected, logging in!')
        login_attempts += 1

    if clickBtn(images['select-wallet-2'], name='sign button', timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts += 1

        if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout=15):
            login_attempts = 0
        return

    if not clickBtn(images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
        if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn',
                    threshold=ct['select_wallet_buttons']):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)
    else:
        pass
        # print('sleep in case there is no metamask text removed')
        # time.sleep(20)

    if clickBtn(images['select-wallet-2'], name='signBtn', timeout=20):
        login_attempts += 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        # time.sleep(25)
        if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout=25):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)

    if clickBtn(images['ok'], name='okBtn', timeout=5):
        time.sleep(10)
        if not clickBtn(images['connect-wallet'], name='connectWalletBtn', timeout=10):
            pyautogui.hotkey('ctrl', 'f5')

        pass


def sendHeroesHome():
    if not ch['enable']:
        return
    heroes_positions = []
    for hero in home_heroes:
        hero_positions = positions(hero, threshold=ch['hero_threshold'])
        if not len(hero_positions) == 0:
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)
    # if send-home button exists, the hero is not home
    go_home_buttons = positions(images['send-home'], threshold=ch['home_button_threshold'])
    go_work_buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    for position in heroes_positions:
        if not isHome(position, go_home_buttons):
            print(isWorking(position, go_work_buttons))
            if not isWorking(position, go_work_buttons):
                print('hero not working, sending him home')
                moveToWithRandomness(go_home_buttons[0][0] + go_home_buttons[0][2] / 2, position[1] + position[3] / 2,
                                     1)
                pyautogui.click()
            else:
                print('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')


def refreshHeroes():
    logger('🏢 Search for heroes to work')

    goToHeroes()

    if c['select_heroes_mode'] == "full":
        logger('⚒️ Sending heroes with full stamina bar to work', 'green')
    elif c['select_heroes_mode'] == "green":
        logger('⚒️ Sending heroes with green stamina bar to work', 'green')

    buttonsClicked = 1
    empty_scrolls_attempts = c['scroll_attemps']

    while empty_scrolls_attempts > 0:
        if c['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons()
        elif c['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons()

        sendHeroesHome()

        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        time.sleep(2)
    logger('💪 {} heroes sent to work'.format(hero_clicks))
    goToGame()


def send_work():
    if c['select_heroes_mode'] == 'all':
        logger('⚒️ Sending all heroes to work', 'green')
        goToHeroes()
        time.sleep(2)
        clickBtn(images['all'])
        time.sleep(1)
        goToGame()
    else:
        refreshHeroes()


def main():

    global clickBtn
    time.sleep(5)
    t = c['time_intervals']

    windows = []

    for w in pygetwindow.getWindowsWithTitle('Bombcrypto'):
        windows.append({
            "window": w,
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "check_for_captcha": 0,
            "refresh_heroes": 0
        })

    while True:
        count = total = 0
        for last in windows:
            last["window"].activate()
            now = time.time()

            for n in enumerate(pygetwindow.getWindowsWithTitle('Bombcrypto')):
                total += 1
            print()
            logger(f'Activating Bot Window {count + 1}')
            if count > total:
                count = 0
            count += 1
            print()  # For space between cicles
            # new check login
            logged = False
            while not logged:

                # check for Blackscreen in login screen when we don't have any button.
                if not check_login(images['network']):
                    if not check_login(images['ok']):
                        if not check_login(images['connect-wallet']):
                            if not check_login(images['treasure-hunt-icon']):
                                if not check_login(images['go-back-arrow']):
                                    if not check_login(images['x']):
                                        logger('Black Screen Found. Reseting Browser')
                                        last["window"].activate()
                                        pyautogui.hotkey('ctrl', 'f5')
                                        time.sleep(10)
                                    else:
                                        clickBtn(images['x'])
                                        logged = True

                                else:
                                    logged = True
                            else:
                                logged = True
                        else:
                            login()
                    else:
                        logger('Ok button Found, refreshing page and trying to login again.')
                        pyautogui.hotkey('ctrl', 'f5')
                        time.sleep(10)
                else:
                    logger('Network error found. Check if metamask is connected to Binance Smart Chain.')
                    clickBtn(images['ok'])
                    time.sleep(10)  # Wait for new wallet connect

            if logged:
                logger('<Game logged sucessfully>')

            if last['heroes'] == 0 or now - last["heroes"] > addRandomness(t['send_heroes_for_work'] * 60):
                logger('💪 Sending heroes to work')
                send_work()
                last['heroes'] = now
                last["refresh_heroes"] = now
            else:
                logger('💪 Heroes already working or resting until next reset.')

            # Refresh Heroes to avoid disconnects.
            logger('Preparing Heroes Refresh.')
            if now - last["refresh_heroes"] > addRandomness(t['refresh_heroes_positions'] * 60):
                last["refresh_heroes"] = now
                refreshHeroesPositions()
            next_reboot = last["heroes"]+(t["send_heroes_for_work"]*60)
            next_refresh = last["refresh_heroes"]+(t["refresh_heroes_positions"]*60)

            logger(f'Time for next hero REBOOT: {datetime.fromtimestamp(next_reboot).strftime("%H:%M:%S")}. Current Set: {t["send_heroes_for_work"]} minutes.')
            logger(f'Time for next hero REFRESH: {datetime.fromtimestamp(next_refresh).strftime("%H:%M:%S")}. Current Set: {t["refresh_heroes_positions"]} minutes.')

            logger(None, progress_indicator=True)

            sys.stdout.flush()

            time.sleep(1)


main()
