# -*- coding: utf-8 -*-    
from cv2 import cv2
# import simpleaudio


from os import listdir
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
import re
import winsound
import requests
import telepot
import os

import pytesseract as ocr
from PIL import Image
from pyclick import HumanClicker

TELEGRAM_BOT_TOKEN = 'TOKEN'
TELEGRAM_CHAT_ID  = 'CHAT_ID'

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def telegram_bot_sendtext(bot_message, num_try = 0):
    global bot
    try:
        return bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=bot_message)
    except:
        if num_try == 1:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            return telegram_bot_sendtext(bot_message, 1)
        return 0

def telegram_bot_sendphoto(photo_path, num_try = 0):
    global bot
    try:
        return bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(photo_path, 'rb'))
    except:
        if num_try == 1:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            return telegram_bot_sendphoto(photo_path, 1)
        return 0

# initialize HumanClicker object
hc = HumanClicker()

# Any duration less than this is rounded to 0.0 to instantly move the mouse.
pyautogui.MINIMUM_DURATION = 0.1
# Minimal number of seconds to sleep between mouse moves.
pyautogui.MINIMUM_SLEEP = 0.1
# The number of seconds to pause after EVERY public function call.
pyautogui.PAUSE = 2

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
================ Please, consider buying me an coffe :) =================
=========================================================================
============== 0xbd06182D8360FB7AC1B05e871e56c76372510dDf ===============
===== https://www.paypal.com/donate?hosted_button_id=JVYSC6ZYCNQQQ ======
=========================================================================

>>---> Press ctrl + c to kill the bot.

>>---> Some configs can be fount in the config.yaml file."""


print(cat)
test = telegram_bot_sendtext("🔌 Bot inicializado. \n\n 💰 É hora de faturar alguns BCoins!!!")


# bell_sound = simpleaudio.WaveObject.from_wave_file("bell.wav")


if __name__ == '__main__':
    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)

ct = c['threshold']
ch = c['home']

if not ch['enable']:
    print('>>---> Home feature not enabled')
print('\n')

pyautogui.PAUSE = c['time_intervals']['interval_between_moviments']

pyautogui.FAILSAFE = False
hero_clicks = 0
login_attempts = 0
last_log_is_progress = False
saldo_atual = 0.0

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
    # pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)
    hc.move((int(x), int(y)), t)

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
puzzle_img = cv2.imread('targets/puzzle.png')
piece = cv2.imread('targets/piece.png')
robot = cv2.imread('targets/robot.png')
slider = cv2.imread('targets/slider.png')

def findPuzzlePieces(result, piece_img, threshold=0.5):
    piece_w = piece_img.shape[1]
    piece_h = piece_img.shape[0]
    yloc, xloc = np.where(result >= threshold)

    r= []
    for (piece_x, piece_y) in zip(xloc, yloc):
        r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])
        r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])

    r, weights = cv2.groupRectangles(r, 1, 0.2)

    if len(r) < 2:
        return findPuzzlePieces(result, piece_img,threshold-0.01)

    if len(r) == 2:
        return r

    if len(r) > 2:
        logger('💀 Overshoot by %d' % len(r))

        return r

def getRightPiece(puzzle_pieces):
    xs = [row[0] for row in puzzle_pieces]
    index_of_right_rectangle = xs.index(max(xs))

    right_piece = puzzle_pieces[index_of_right_rectangle]
    return right_piece

def getLeftPiece(puzzle_pieces):
    xs = [row[0] for row in puzzle_pieces]
    index_of_left_rectangle = xs.index(min(xs))

    left_piece = puzzle_pieces[index_of_left_rectangle]
    return left_piece

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

def getPiecesPosition(t = 150):
    popup_pos = positions(robot)
    if len(popup_pos) == 0:
        return None
    rx, ry, _, _ = popup_pos[0]

    w = 380
    h = 200
    x_offset = -40
    y_offset = 65

    y = ry + y_offset
    x = rx + x_offset

    img = printSreen()
    #TODO tirar um poco de cima

    cropped = img[ y : y + h , x: x + w]
    blurred = cv2.GaussianBlur(cropped, (3, 3), 0)
    edges = cv2.Canny(blurred, threshold1=t/2, threshold2=t,L2gradient=True)
    # img = cv2.Laplacian(img,cv2.CV_64F)

    # gray_piece_img = cv2.cvtColor(piece, cv2.COLOR_BGR2GRAY)
    piece_img = cv2.cvtColor(piece, cv2.COLOR_BGR2GRAY)
    # piece_img = cv2.Canny(gray_piece_img, threshold1=t/2, threshold2=t,L2gradient=True)
    # result = cv2.matchTemplate(edges,piece_img,cv2.TM_CCOEFF_NORMED)
    result = cv2.matchTemplate(edges,piece_img,cv2.TM_CCORR_NORMED)

    puzzle_pieces = findPuzzlePieces(result, piece_img)

    if puzzle_pieces is None:
        return None

    # show(puzzle_pieces, edges)
    # exit()

    absolute_puzzle_pieces = []
    for i, puzzle_piece in enumerate(puzzle_pieces):
        px, py, pw, ph = puzzle_piece
        absolute_puzzle_pieces.append( [ x + px, y + py, pw, ph])

    absolute_puzzle_pieces = np.array(absolute_puzzle_pieces)
    # show(absolute_puzzle_pieces)
    return absolute_puzzle_pieces

def getSliderPosition():
    slider_pos = positions(slider)
    if len (slider_pos) == 0:
        return None
    x, y, w, h = slider_pos[0]
    position = [x+w/2,y+h/2]
    return position

def saveCaptchaSolution(img, pos):
    path = "./captchas-saved/{}.png".format(str(time.time()))
    rx, ry, _, _ = pos

    w = 580
    h = 400
    x_offset = -140
    y_offset = 65

    y = ry + y_offset
    x = rx + x_offset
    cropped = img[ y : y + h , x: x + w]

    # cv2.imshow('img',cropped)
    # cv2.waitKey(5000)
    # exit()

    cv2.imwrite(path, cropped)
    #TODO tirar um poco de cima


def alertCaptcha():
    current = printSreen()
    popup_pos = positions(robot,img=current)

    if len(popup_pos) == 0:
        logger('Captcha box não encontrado')
        return "not-found"

    test = telegram_bot_sendtext("⚠️ ATENÇÃO! \n\n 🧩 RESOLVER NOVO CAPTCHA!")
    logger('Captcha!')
    # bell_sound.play()
    winsound.PlaySound ('bell.wav', winsound .SND_ASYNC);

    #linha para testes

    slider_start_pos = getSliderPosition()
    if slider_start_pos is None:
        logger('Posição do slider do captcha não encontrado')
        return

    
    slider_mov = 35
    slider_size = positions(images['slider_size_1'], threshold=0.9)

    #obten o quanto de pixels o ponteiro tem que arrastar de acordo com o tamanho do slider que aparece
    numero_sliders = 8 # o número de repetições é a quantidade de imagens do slider-size que tenho + 1
    for i in range(1, numero_sliders): 
        slider_size = positions(images[f'slider_size_{i}'], threshold=0.9)
        if(len(slider_size) > 0):
            slider_mov = slider_mov + (10 * i)
            break
        time.sleep(1)
    
    if(len(slider_size) == 0):
        logger('Tamanho do slider do captcha não encontrado!')
        return

    slider_positions = []
    x,y = slider_start_pos
    for i in range(5):
        if i == 0:
            # pyautogui.moveTo(x, y, 1)
            moveToWithRandomness(x, y, 1)
            pyautogui.mouseDown()

            #faz o primeiro movimento e volta para abrir o primeiro item
            pyautogui.moveTo(x + slider_mov, y, 0.15)
            pyautogui.moveTo(x, y, 1)
            slider_positions.append((x, y))
        else:
            slider_start_pos = getSliderPosition()
            x,y = slider_start_pos
            pyautogui.moveTo(x, y, 0.15)
            # time.sleep(0.5)

            slider_positions.append((x + slider_mov, y))
            pyautogui.moveTo(x + slider_mov, y, 0.15)

        time.sleep(0.5)
        #encontra a posição do captcha inteiro
        captcha_scshot = pyautogui.screenshot(region=(popup_pos[0][0] - 120, popup_pos[0][1] + 80, popup_pos[0][2]*1.9, popup_pos[0][3]*8.3))
        img_captcha_dir = os.path.dirname(os.path.realpath(__file__)) + r'\targets\captcha1.png'
        captcha_scshot.save(img_captcha_dir)

        #envia a foto do captcha
        telegram_bot_sendtext(f'Imagem /{i + 1}')
        telegram_bot_sendphoto(img_captcha_dir)

    logger('Esperando pela resposta do usuário...')
    qtd_messages_sended = len(bot.getUpdates())
    user_response = 0
    # await user to response
    try:
        while True:
            messages_now = bot.getUpdates()
            if len(messages_now) > qtd_messages_sended and messages_now[len(messages_now) -1].message.text.replace('/','').isdigit:
                user_response = int(messages_now[len(messages_now) -1].message.text.replace('/',''))
                break
                
            time.sleep(4)
    except:
        logger('Sem resposta do usuário!')

    if(user_response == 0):
        logger('Sem resposta do usuário!')
        return

    logger(f"usuario escolheu o numero {user_response}")

    pyautogui.moveTo(slider_positions[user_response-1][0], slider_positions[user_response-1][1], 0.5)
    pyautogui.moveTo(slider_positions[user_response-1][0] + 4, slider_positions[user_response-1][1] + 3, 0.5)
    # time.sleep(0.5)
    pyautogui.mouseUp()

    time.sleep(2)
    if(len(positions(robot)) == 0):
        telegram_bot_sendtext('Resolvido')
    else:
        telegram_bot_sendtext('Falhou')

    #end da linha para testes

    # i=0
    # while True:
    #     i = i + 1
    #     last = current
    #     last_popup_pos = popup_pos
    #     current = printSreen()
    #     popup_pos = positions(robot,img=current)
	# 
    #     if len(popup_pos) == 0:
    #         logger('solved!')
    #         saveCaptchaSolution(last, last_popup_pos[0])
    #         break


#    #TODO adicionar a funçao de checar se um botao esta visive
#    # pro bot passar um tempinho fazendo um polling dps q a funçao eh invocada.
#    logger('🧩 Checking for captcha')
#    pieces_start_pos = getPiecesPosition()
#    if pieces_start_pos is None :
#        return "not-found"
#    slider_start_pos = getSliderPosition()
#    if slider_start_pos is None:
#        logger('🧩 slider_start_pos')
#        return "fail"
#
#    x,y = slider_start_pos
#    pyautogui.moveTo(x,y,1)
#    pyautogui.mouseDown()
#    pyautogui.moveTo(x+300 ,y,0.5)
#    pieces_end_pos = getPiecesPosition()
#    if pieces_end_pos is None:
#        logger('🧩 pieces_end_pos')
#        return "fail"
#
#    piece_start, _, _, _ = getLeftPiece(pieces_start_pos)
#    piece_end, _, _, _ = getRightPiece(pieces_end_pos)
#    piece_middle, _, _, _  = getRightPiece(pieces_start_pos)
#    slider_start, _, = slider_start_pos
#    slider_end_pos = getSliderPosition()
#    if slider_end_pos is None:
#        logger('🧩 slider_end_pos')
#        return "fail"
#
#    slider_end, _ = slider_end_pos
#
#    piece_domain = piece_end - piece_start
#    middle_piece_in_percent = (piece_middle - piece_start)/piece_domain
#
#    slider_domain = slider_end - slider_start
#    slider_awnser = slider_start + (middle_piece_in_percent * slider_domain)
#    # arr = np.array([[int(piece_start),int(y-20),int(10),int(10)],[int(piece_middle),int(y-20),int(10),int(10)],[int(piece_end-20),int(y),int(10),int(10)],[int(slider_awnser),int(y),int(20),int(20)]])
#
#    pyautogui.moveTo(slider_awnser,y,0.5)
#    pyautogui.mouseUp()
#
#    return True
#    # show(arr)

def clickBtn(img,name=None, timeout=3, threshold = ct['default']):
    logger(None, progress_indicator=True)
    if not name is None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    clicked = False
    while(not clicked):
        matches = positions(img, threshold=threshold)
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
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        # mudar moveto pra w randomness
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[2]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:,:,:3]

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

    commoms = positions(images['commom-text'], threshold = ct['commom'])
    if (len(commoms) == 0):
        return
    x,y,w,h = commoms[len(commoms)-1]
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

    alertCaptcha()
    #TODO tirar o sleep quando colocar o pulling
    time.sleep(1)
    clickBtn(images['hero-icon'])
    time.sleep(1)
    alertCaptcha()

def goToGame():
    # in case of server overload popup
    clickBtn(images['x'])
    # time.sleep(3)
    clickBtn(images['x'])

    clickBtn(images['treasure-hunt-icon'])

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
    l = l - 51
    m = m + 90
    n = n + 100

    myScreen = pyautogui.screenshot(region=(k, l, m, n))
    img_dir = os.path.dirname(os.path.realpath(__file__)) + r'\targets\saldo1.png'
    myScreen.save(img_dir)
    saldoApurado = ocr.image_to_string(Image.open(img_dir))

    saldoApurado = re.sub("[^\d\.]", "", saldoApurado)
    if saldoApurado == '':
        saldoApurado = 0.0
    if float(saldoApurado) > float(saldo_atual):
        saldoApurado = saldoApurado.strip()

        enviar = ('🚨 \n Seu saldo aumentou. \n Valor atual: $'+saldoApurado+' Bcoins \n 🚀🚀🚀')
        test = telegram_bot_sendtext(enviar)
        #test = telegram_bot_sendtext(saldoApurado)
        #print(enviar)
        saldo_atual = saldoApurado
    else:
        print("Saldo zero")
        telegram_bot_sendtext("ATENÇÂO: Saldo reconhecido 0, pode estar havendo instabilidade no servidor.")

    clickBtn(images['x'])

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
        return

    if clickBtn(images['connect-wallet'], name='connectWalletBtn', timeout = 10):
        alertCaptcha()
        login_attempts = login_attempts + 1
        logger('🎉 Connect wallet button detected, logging in!')
        #TODO mto ele da erro e poco o botao n abre
        # time.sleep(10)

    if clickBtn(images['select-wallet-2'], name='sign button', timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout = 15):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        return
        # click ok button

    elif not clickBtn(images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
        if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', threshold  = ct['select_wallet_buttons'] ):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo 
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)

    elif clickBtn(images['select-wallet-2'], name='signBtn', timeout = 20):
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

    # goToHeroes()

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

def decobreScreen():

    # 3 metamask
    if len(positions(images['select-wallet-2'], threshold=0.75)) > 0:
        return 3
    # 7 error popup
    elif len(positions(images['ok'], threshold=ct['default'])) > 0:
        return 7
    # 2 captcha
    elif(getPiecesPosition() is not None):
        return 2
    # 1 tela de login
    elif len(positions(images['connect-wallet'], threshold=ct['default'])) > 0:
        return 1
    # 4 pagina main
    elif len(positions(images['hero-icon'], threshold=ct['default'])) > 0:
        return 4
    # 5 pagina herois
    elif len(positions(images['go-work'], threshold=ct['default'])) > 0:
        return 5
    # 6 pagina trabalho
    elif len(positions(images['go-back-arrow'], threshold=ct['default'])) > 0:
        return 6
    # 8 new map
    elif len(positions(images['new-map'], threshold=ct['default'])) > 0:
        return 8

    # 0 sem tela definida
    return 0

def main():
    time.sleep(5)
    t = c['time_intervals']

    last = {
    "login" : 0,
    "heroes" : 0,
    "ssaldo" :0,
    "new_map" : 0,
    "check_for_captcha" : 0,
    "refresh_heroes" : 0
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

        # 0 sem tela definida
        if screen == 0:
            logger("Não reconheceu nenhuma tela!")
            time.sleep(10)
            continue
        elif screen == 1: # 1 tela de login
            # ja tentou fazer login e não conseguiu
            if screen == screenAnt :
                # tentamos fazer login manualmente
                # tenta abrir a tela de login metamask que provavelmente esta em segundo plano
                logger('Trying manual login...')
                if not clickBtn(images['metamask-ext-ico'], timeout = 10):
                    if not clickBtn(images['metamask-taskbar'], timeout = 10):
                        if clickBtn(images['connect-wallet'], name='connectWalletBtn', timeout = 10):
                            logger('Connect wallet button detected, logging in!')

            elif (now - last["login"]) > (t['check_for_login'] * 60):
                logger("Checking if game has disconnected.")
                sys.stdout.flush()
                last["login"] = now
                login()
        elif screen == 2: # 2 captcha
            # if (now - last["check_for_capcha"]) > (t['check_for_capcha'] * 60):
                #last["check_for_capcha"] = now
            logger('Checking for capcha.')
            # solveCapcha()
            alertCaptcha()
        elif screen == 3: # 3 metamask
            logger('Clicking MetaMask Sign button.')
            clickBtn(images['select-wallet-2'], name='sign button', timeout=8)
            if screenAnt == 1 and screen == 1 :
                time.sleep(15)
        elif screen == 4: # 4 pagina main
            clickBtn(images['hero-icon'])
        elif screen == 5: # 5 pagina herois
            if (now - last["heroes"]) > (t['send_heroes_for_work'] * 60):
                last["heroes"] = now
                logger('Sending heroes to work.')
                refreshHeroes()
        elif screen == 6: # 6 pagina trabalho
            logger('Working heroes screen.')
            if last["heroes"] == 0 :
                last["heroes"] = now
            if last["refresh_heroes"] == 0 :
                last["refresh_heroes"] = last["heroes"]
            if (now - last["refresh_heroes"]) > (t['refresh_heroes_positions'] * 60) :
                last["refresh_heroes"] = now
                logger('Refreshing Heroes Positions.')
                refreshHeroesPositions()
        elif screen == 7: # 7 error popup
            clickBtn(images['ok'], name='okBtn', timeout=5)
        elif screen == 8: # 8 new map
            if (now - last["new_map"]) > t['check_for_new_map_button']:
                last["new_map"] = now
                if clickBtn(images['new-map']):
                    loggerMapClicked()

        #opção de quando os herois vão dormir, voltar para tela main
        if screen == 6 and (now - last["refresh_heroes"]) > (t['refresh_heroes_positions'] * 60) :
                last["refresh_heroes"] = now
                logger('Refreshing Heroes Positions.')
                refreshHeroesPositions()
        if screen == 6 and (now - last["heroes"]) > (t['send_heroes_for_work'] * 60):
            clickBtn(images['go-back-arrow'])
            # informa que saiu da pagina de trabalho para pagina main
            screen = 4

        if screen == 6 and ((now - last["ssaldo"]) > (addRandomness(t['get_saldo'] * 60))):
            last["ssaldo"] = now
            goSaldo()

        screenAnt = screen

        #clickBtn(teasureHunt)
        logger(None, progress_indicator=True)

        # se os herois tiverem trabalhando, faz um sleed pelo tempo do refresh dos herois para econimizar processamento
        if screen == 6 :
            time.sleep(t['refresh_heroes_positions'] * 60)

        sys.stdout.flush()

        time.sleep(1)

ocr.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
main()
# sendHeroesHome()


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
# pip uninstall opencv-python

# pip install --upgrade opencv-python==4.5.3.56
