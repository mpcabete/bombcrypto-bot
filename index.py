# -*- coding: utf-8 -*-
from cv2 import cv2

from captcha.solveCaptcha import solveCaptcha

from os import listdir
import os
from src.logger import logger, loggerMapClicked
from random import randint
from random import random

import numpy as np
import mss
import pyautogui
import time
import sys

import yaml
import telegram
from datetime import datetime
from pyclick import HumanClicker
from numpy import asarray

# initialize HumanClicker object
hc = HumanClicker()

# Any duration less than this is rounded to 0.0 to instantly move the mouse.
pyautogui.MINIMUM_DURATION = 0.1
# Minimal number of seconds to sleep between mouse moves.
pyautogui.MINIMUM_SLEEP = 0.1
# The number of seconds to pause after EVERY public function call.
pyautogui.PAUSE = 2


TELEGRAM_BOT_TOKEN = "TOKEN"
TELEGRAM_CHAT_ID = "CHAT_ID"

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


def telegram_bot_sendtext(bot_message, num_try=0):
    global bot
    try:
        return bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=bot_message)
    except:
        if num_try == 1:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            return telegram_bot_sendtext(bot_message, 1)
        return 0


def telegram_bot_sendphoto(photo_path, num_try=0):
    global bot
    try:
        return bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(photo_path, "rb"))
    except:
        if num_try == 1:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            return telegram_bot_sendphoto(photo_path, 1)
        return 0


test = telegram_bot_sendtext(
    "🔌 Bot inicializado. \n\n 💰 É hora de faturar alguns BCoins!!!"
)

saldo_atual = 0.0

if __name__ == "__main__":
    stream = open("config.yaml", "r")
    c = yaml.safe_load(stream)

ct = c["threshold"]
ch = c["home"]

if not ch["enable"]:
    print(">>---> Home feature not enabled")
print("\n")

pyautogui.PAUSE = c["time_intervals"]["interval_between_moviments"]

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
    # pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)
    hc.move((int(x), int(y)), t)


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[: -len(suffix)]
    return input_string


def load_images():
    file_names = listdir("./targets/")
    targets = {}
    for file in file_names:
        path = "targets/" + file
        targets[remove_suffix(file, ".png")] = cv2.imread(path)

    return targets


images = load_images()


def loadHeroesToSendHome():
    file_names = listdir("./targets/heroes-to-send-home")
    heroes = []
    for file in file_names:
        path = "./targets/heroes-to-send-home/" + file
        heroes.append(cv2.imread(path))

    print(">>---> %d heroes that should be sent home loaded" % len(heroes))
    return heroes


if ch["enable"]:
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
full_stamina = cv2.imread("targets/full-stamina.png")

robot = cv2.imread("targets/robot.png")
# puzzle_img = cv2.imread('targets/puzzle.png')
# piece = cv2.imread('targets/piece.png')
slider = cv2.imread("targets/slider.png")


def show(rectangles, img=None):

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255, 255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow("img", img)
    cv2.waitKey(0)


def clickBtn(img, name=None, timeout=3, threshold=ct["default"]):
    logger(None, progress_indicator=True)
    if not name is None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    clicked = False
    while not clicked:
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


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:, :, :3]


def positions(target, threshold=ct["default"], img=None):
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

    commoms = positions(images["commom-text"], threshold=ct["commom"])
    if len(commoms) == 0:
        return
    x, y, w, h = commoms[len(commoms) - 1]
    #
    moveToWithRandomness(x, y, 1)

    if not c["use_click_and_drag_instead_of_scroll"]:
        pyautogui.scroll(-c["scroll_size"])
    else:
        pyautogui.dragRel(0, -c["click_and_drag_amount"], duration=1, button="left")


def clickButtons():
    buttons = positions(images["go-work"], threshold=ct["go_to_work_btn"])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger("too many hero clicks, try to increase the go_to_work_btn threshold")
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

    green_bars = positions(images["green-bar"], threshold=ct["green_bar"])
    logger("🟩 %d green bars detected" % len(green_bars))
    buttons = positions(images["go-work"], threshold=ct["go_to_work_btn"])
    logger("🆗 %d buttons detected" % len(buttons))

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger("🆗 %d buttons with green bar detected" % len(not_working_green_bars))
        logger("👆 Clicking in %d heroes" % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        moveToWithRandomness(x + offset + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        if hero_clicks > 20:
            logger(
                "⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold"
            )
            return
        # cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)


def clickFullBarButtons():
    offset = 100
    full_bars = positions(images["full-stamina"], threshold=ct["default"])
    buttons = positions(images["go-work"], threshold=ct["go_to_work_btn"])

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        logger("👆 Clicking in %d heroes" % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        moveToWithRandomness(x + offset + (w / 2), y + (h / 2), 1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1

    return len(not_working_full_bars)


def goToHeroes():
    if clickBtn(images["go-back-arrow"]):
        global login_attempts
        login_attempts = 0

    solveCaptcha()
    # TODO tirar o sleep quando colocar o pulling
    time.sleep(1)
    clickBtn(images["hero-icon"])
    time.sleep(1)
    solveCaptcha()


def goToGame():
    # in case of server overload popup
    clickBtn(images["x"])
    # time.sleep(3)
    clickBtn(images["x"])

    clickBtn(images["treasure-hunt-icon"])


def refreshHeroesPositions():

    logger("🔃 Refreshing Heroes Positions")
    clickBtn(images["go-back-arrow"])
    clickBtn(images["treasure-hunt-icon"])

    # time.sleep(3)
    clickBtn(images["treasure-hunt-icon"])


def login():
    global login_attempts
    logger("😿 Checking if game has disconnected")

    if login_attempts > 3:
        logger("🔃 Too many login attempts, refreshing")
        login_attempts = 0
        pyautogui.hotkey("ctrl", "f5")
        return

    if clickBtn(images["connect-wallet"], name="connectWalletBtn", timeout=10):
        # solveCaptcha()
        login_attempts = login_attempts + 1
        logger("🎉 Connect wallet button detected, logging in!")
        # TODO mto ele da erro e poco o botao n abre
        # time.sleep(10)

def sendHeroesHome():
    if not ch["enable"]:
        return
    heroes_positions = []
    for hero in home_heroes:
        hero_positions = positions(hero, threshold=ch["hero_threshold"])
        if not len(hero_positions) == 0:
            # TODO maybe pick up match with most wheight instead of first
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print("No heroes that should be sent home found.")
        return
    print(" %d heroes that should be sent home found" % n)
    # if send-home button exists, the hero is not home
    go_home_buttons = positions(
        images["send-home"], threshold=ch["home_button_threshold"]
    )
    # TODO pass it as an argument for both this and the other function that uses it
    go_work_buttons = positions(images["go-work"], threshold=ct["go_to_work_btn"])

    for position in heroes_positions:
        if not isHome(position, go_home_buttons):
            print(isWorking(position, go_work_buttons))
            if not isWorking(position, go_work_buttons):
                print("hero not working, sending him home")
                moveToWithRandomness(
                    go_home_buttons[0][0] + go_home_buttons[0][2] / 2,
                    position[1] + position[3] / 2,
                    1,
                )
                pyautogui.click()
            else:
                print("hero working, not sending him home(no dark work button)")
        else:
            print("hero already home, or home full(no dark home button)")


def refreshHeroes():
    logger("🏢 Search for heroes to work")

    # goToHeroes()

    if c["select_heroes_mode"] == "full":
        logger("⚒️ Sending heroes with full stamina bar to work", "green")
    elif c["select_heroes_mode"] == "green":
        logger("⚒️ Sending heroes with green stamina bar to work", "green")
    else:
        logger("⚒️ Sending all heroes to work", "green")

    buttonsClicked = 1
    empty_scrolls_attempts = c["scroll_attemps"]

    while empty_scrolls_attempts > 0:
        if c["select_heroes_mode"] == "full":
            buttonsClicked = clickFullBarButtons()
        elif c["select_heroes_mode"] == "green":
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked = clickButtons()

        sendHeroesHome()

        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        time.sleep(2)
    logger("💪 {} heroes sent to work".format(hero_clicks))
    goToGame()

def goSaldo():
    global saldo_atual
    clickBtn(images['consultar-saldo'])
    #test = telegram_bot_sendtext("Saldo de BCoins atualizado:")

    i = 10
    coins_pos = positions(images['coin-icon'], threshold=ct['default'])
    while(len(coins_pos) == 0):
        if i <= 0:
            break
        i = i - 1
        coins_pos = positions(images['coin-icon'], threshold=ct['default'])
        time.sleep(5)
    
    if(len(coins_pos) == 0):
        logger("Saldo não encontrado.")
        clickBtn(images['x'])
        return

    # a partir da imagem do bcoin calcula a area do quadrado para print
    k,l,m,n = coins_pos[0]
    k = k - 44
    l = l + 130
    m = 200
    n = 50

    myScreen = pyautogui.screenshot(region=(k, l, m, n))
    img_dir = os.path.dirname(os.path.realpath(__file__)) + r'\targets\saldo1.png'
    myScreen.save(img_dir)
    time.sleep(2)
    enviar = ('🚨 Seu saldo Bcoins 🚀🚀🚀')
    test = telegram_bot_sendtext(enviar)
    telegram_bot_sendphoto(img_dir)

    clickBtn(images['x'])

def getDifference(then, now=datetime.now(), interval="horas"):

    duration = now - then
    duration_in_s = duration.total_seconds()

    # Date and Time constants
    yr_ct = 365 * 24 * 60 * 60  # 31536000
    day_ct = 24 * 60 * 60  # 86400
    hour_ct = 60 * 60  # 3600
    minute_ct = 60

    def yrs():
        return divmod(duration_in_s, yr_ct)[0]

    def days():
        return divmod(duration_in_s, day_ct)[0]

    def hrs():
        return divmod(duration_in_s, hour_ct)[0]

    def mins():
        return divmod(duration_in_s, minute_ct)[0]

    def secs():
        return duration_in_s

    return {
        "anos": int(yrs()),
        "dias": int(days()),
        "horas": int(hrs()),
        "minutos": int(mins()),
        "segundos": int(secs()),
    }[interval]


def tempoGastoParaComletarMapa():
    try:
        data_inicio_mapa = None
        caminho = (
            os.path.dirname(os.path.realpath(__file__)) + r"\savedvars\tempo_mapa.txt"
        )
        with open(caminho, "r") as text_file:
            data_inicio_mapa = text_file.readline()
            if data_inicio_mapa == "":
                data_inicio_mapa = datetime.now()

            if not isinstance(data_inicio_mapa, datetime):
                data_inicio_mapa = datetime.strptime(
                    data_inicio_mapa, "%Y-%m-%d %H:%M:%S.%f"
                )
            intervalo = "horas"
            horas_gastas = getDifference(
                data_inicio_mapa, now=datetime.now(), interval=intervalo
            )
            if horas_gastas == 0:
                intervalo = "minutos"
                horas_gastas = getDifference(
                    data_inicio_mapa, now=datetime.now(), interval=intervalo
                )
            if horas_gastas == 0:
                intervalo = "segundos"
                horas_gastas = getDifference(
                    data_inicio_mapa, now=datetime.now(), interval=intervalo
                )

            telegram_bot_sendtext(
                f"Demoramos {horas_gastas} {intervalo} para concluir o mapa."
            )
        with open(caminho, "w") as text_file_write:
            data_inicio_mapa = datetime.now()
            text_file_write.write(str(data_inicio_mapa))

    except:
        logger("Não conseguiu obter informações do tempo de conclusão do mapa.")


def decobreScreen():

    # 3 metamask
    if len(positions(images["select-wallet-2"], threshold=0.75)) > 0:
        return 3
    # 7 error popup
    elif len(positions(images["ok"], threshold=ct["default"])) > 0:
        return 7
    # 2 captcha
    elif len(positions(images["robot"], threshold=ct["default"])) > 0:
        return 2
    # 1 tela de login
    elif len(positions(images["connect-wallet"], threshold=ct["default"])) > 0:
        return 1
    # 4 pagina main
    elif len(positions(images["hero-icon"], threshold=ct["default"])) > 0:
        return 4
    # 5 pagina herois
    elif len(positions(images["go-work"], threshold=ct["default"])) > 0:
        return 5
    # 8 new map
    elif len(positions(images["new-map"], threshold=ct["default"])) > 0:
        return 8
    # 6 pagina trabalho
    elif len(positions(images["go-back-arrow"], threshold=ct["default"])) > 0:
        return 6

    # 0 sem tela definida
    return 0


def main():
    time.sleep(5)
    t = c["time_intervals"]

    last = {
        "login": 0,
        "heroes": 0,
        "ssaldo" :0,
        "new_map": 0,
        "check_for_captcha": 0,
        "refresh_heroes": 0,
    }

    # 0 sem tela definida
    # 1 tela de login
    # 2 captcha
    # 3 metamask
    # 4 pagina main
    # 5 pagina herois
    # 6 pagina trabalho
    # 7 error popup
    # 8 new map

    screenAnt = -1
    while True:

        now = time.time()

        screen = decobreScreen()

        try:
            # 0 sem tela definida
            if screen == 0:
                logger("Não reconheceu nenhuma tela!")
                time.sleep(10)
                continue
            elif screen == 1:  # 1 tela de login
                # ja tentou fazer login e não conseguiu
                if screen == screenAnt:
                    # tentamos fazer login manualmente
                    # tenta abrir a tela de login metamask que provavelmente esta em segundo plano
                    logger("Trying manual login...")
                    if not clickBtn(images["metamask-ext-ico"], timeout=10):
                        if not clickBtn(images["metamask-taskbar"], timeout=10):
                            if clickBtn(
                                images["connect-wallet"],
                                name="connectWalletBtn",
                                timeout=10,
                            ):
                                logger("Connect wallet button detected, logging in!")
                    time.sleep(2)

                elif (now - last["login"]) > (t["check_for_login"] * 60):
                    logger("Checking if game has disconnected.")
                    sys.stdout.flush()
                    last["login"] = now
                    login()
            elif screen == 2:  # 2 captcha
                # if (now - last["check_for_capcha"]) > (t['check_for_capcha'] * 60):
                # last["check_for_capcha"] = now
                logger("Checking for capcha.")
                solveCaptcha()
                # alertCaptcha()
            elif screen == 3:  # 3 metamask
                logger("Clicking MetaMask Sign button.")
                clickBtn(images["select-wallet-2"], name="sign button", timeout=8)
                if screenAnt == 1 and screen == 1:
                    time.sleep(15)
            elif screen == 4:  # 4 pagina main
                clickBtn(images["hero-icon"])
            elif screen == 5:  # 5 pagina herois
                if (now - last["heroes"]) > (t["send_heroes_for_work"] * 60):
                    last["heroes"] = now
                    logger("Sending heroes to work.")
                    refreshHeroes()
            elif screen == 6:  # 6 pagina trabalho
                logger("Working heroes screen.")
                if last["heroes"] == 0:
                    last["heroes"] = now
                if last["refresh_heroes"] == 0:
                    last["refresh_heroes"] = last["heroes"]
                if (now - last["refresh_heroes"]) > (
                    t["refresh_heroes_positions"] * 60
                ):
                    last["refresh_heroes"] = now
                    logger("Refreshing Heroes Positions.")
                    refreshHeroesPositions()
            elif screen == 7:  # 7 error popup
                clickBtn(images["ok"], name="okBtn", timeout=5)
            elif screen == 8:  # 8 new map
                if (now - last["new_map"]) > t["check_for_new_map_button"]:
                    last["new_map"] = now
                    if clickBtn(images["new-map"]):
                        tempoGastoParaComletarMapa()
                        loggerMapClicked()
                        telegram_bot_sendtext(f"Completamos mais um mapa!")
                        time.sleep(3)
                        num_jaulas = len(positions(images["jail"], threshold=0.8))
                        if num_jaulas > 0:
                            telegram_bot_sendtext(
                                f"Parabéns temos {num_jaulas} nova(s) jaula(s) no novo mapa 🎉🎉🎉."
                            )

            # opção de quando os herois vão dormir, voltar para tela main
            if screen == 6 and (now - last["refresh_heroes"]) > (
                t["refresh_heroes_positions"] * 60
            ):
                last["refresh_heroes"] = now
                logger("Refreshing Heroes Positions.")
                refreshHeroesPositions()
            if screen == 6 and (now - last["heroes"]) > (
                t["send_heroes_for_work"] * 60
            ):
                clickBtn(images["go-back-arrow"])
                # informa que saiu da pagina de trabalho para pagina main
                screen = 4

            if screen == 6 and ((now - last["ssaldo"]) > (addRandomness(t['get_saldo'] * 60))):
               last["ssaldo"] = now
               goSaldo()
        except:
            continue

        screenAnt = screen

        # clickBtn(teasureHunt)
        logger(None, progress_indicator=True)

        # se os herois tiverem trabalhando, faz um sleed pelo tempo do refresh dos herois para econimizar processamento
        if screen == 6:
            time.sleep(60)

        sys.stdout.flush()

        time.sleep(1)


main()
# sendHeroesHome()


# cv2.imshow('img',sct_img)
# cv2.waitKey()

# chacar se tem o sign antes de aperta o connect wallet ?
# arrumar aquela parte do codigo copiado onde tem q checar o sign 2 vezes ?
# colocar o botao em pt
# melhorar o log
# salvar timestamp dos clickes em newmap em um arquivo
# soh resetar posiçoes se n tiver clickado em newmap em x segundos

# pegar o offset dinamicamente
# clickar so no q nao tao trabalhando pra evitar um loop infinito no final do scroll se ainda tiver um verdinho
# pip uninstall opencv-python

# pip install --upgrade opencv-python==4.5.3.56
