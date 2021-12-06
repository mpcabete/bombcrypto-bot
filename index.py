from cv2 import cv2
from pyclick import HumanClicker
import numpy as np
import mss
import pyautogui
import telegram
import time
import sys
import yaml
import random
import requests

# TODO: add kill bot on button pressed, server maintenance

banner = """
====== Bomb Crypto Bot - Vin35 Version ======
=============================================

            /$$            /$$$$$$  /$$$$$$$ 
           |__/           /$$__  $$| $$____/ 
 /$$    /$$ /$$ /$$$$$$$ |__/  \ $$| $$      
|  $$  /$$/| $$| $$__  $$   /$$$$$/| $$$$$$$ 
 \  $$/$$/ | $$| $$  \ $$  |___  $$|_____  $$
  \  $$$/  | $$| $$  | $$ /$$  \ $$ /$$  \ $$
   \  $/   | $$| $$  | $$|  $$$$$$/|  $$$$$$/
    \_/    |__/|__/  |__/ \______/  \______/ 
                                             
=== Please, consider buying me a coffee :) ===
= 0x29f3f79179C942d227ec38755c0C1Ea4976672C1 =
==============================================

>>---> Press "ctrl + c" to kill the bot.
>>---> Some configs can be fount in the config.yaml file.
"""

print(banner)

stream = open("config.yaml", 'r')
if stream is not None:
    c = yaml.safe_load(stream)
    ct = c['threshold']
    telegram_data = c['telegram']
    metamask_data = c['metamask']
    chest_data = c['value_chests']
    offsets = c['offsets']
    stream.close()
else:
    logger("Config file not found. Exiting.")
    time.sleep(3)
    exit()

data = requests.get('https://raw.githubusercontent.com/vin350/bombcrypto-bot/main/config.yaml')

if data is not None:
    v = yaml.safe_load(data.text)
    version = v['version']
    data.close()
else:
    logger("Version not found. Exiting.")
    time.sleep(3)
    exit()

hc = HumanClicker()
pyautogui.PAUSE = c['time_intervals']['interval_between_movements']

pyautogui.FAILSAFE = False
hero_clicks = 0
login_attempts = 0
general_check_time = 1


go_work_img = cv2.imread('targets/go-work.png')
home_img = cv2.imread('targets/home.png')
arrow_img = cv2.imread('targets/go-back-arrow.png')
full_screen_img = cv2.imread('targets/full_screen.png')
hero_img = cv2.imread('targets/hero-icon.png')
x_button_img = cv2.imread('targets/x.png')
teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
ok_btn_img = cv2.imread('targets/ok.png')
connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
sign_btn_img = cv2.imread('targets/metamask_sign.png')
new_map_btn_img = cv2.imread('targets/new-map.png')
green_bar = cv2.imread('targets/green-bar.png')
full_stamina = cv2.imread('targets/full-stamina.png')
character_indicator = cv2.imread('targets/character_indicator.png')
error_img = cv2.imread('targets/error.png')
metamask_unlock_img = cv2.imread('targets/unlock_metamask.png')
metamask_cancel_button = cv2.imread('targets/metamask_cancel_button.png')
puzzle_img = cv2.imread('targets/puzzle.png')
piece = cv2.imread('targets/piece.png')
robot = cv2.imread('targets/robot.png')
slider = cv2.imread('targets/slider.png')
chest_button = cv2.imread('targets/treasure_chest.png')
coin_icon = cv2.imread('targets/coin.png')
maintenance_popup = cv2.imread('targets/maintenance.png')
chest1 = cv2.imread('targets/chest1.png')
chest2 = cv2.imread('targets/chest2.png')
chest3 = cv2.imread('targets/chest3.png')
chest4 = cv2.imread('targets/chest4.png')

# Initialize telegram
if telegram_data['telegram_mode'] == True:
    try:
        TBot = telegram.Bot(token=telegram_data["telegram_bot_key"])
    except:
        logger("Bot not initialized! See configuration file.")

def sendTelegramMessage(message):
    if telegram_data['telegram_mode'] == False:
        return
    try:
        if(len(telegram_data["telegram_chat_id"]) > 0):
            for chat_id in telegram_data["telegram_chat_id"]:
                TBot.send_message(text=message, chat_id=chat_id)
    except:
        logger("Unable to send telegram message. See configuration file.")

def sendPossibleAmountReport(baseImage):
    if telegram_data['telegram_mode'] == False:
        return
    c1 = len(positions(chest1, ct['chest'], baseImage, True))
    c2 = len(positions(chest2, ct['chest'], baseImage, True))
    c3 = len(positions(chest3, ct['chest'], baseImage, True))
    c4 = len(positions(chest4, ct['chest'], baseImage, True))
    
    value1 = c1 * chest_data["value_chest1"]
    value2 = c2 * chest_data["value_chest2"]
    value3 = c3 * chest_data["value_chest3"]
    value4 = c4 * chest_data["value_chest4"]

    total = value1 + value2 + value3 + value4

    report = """
Possible quantity chest per type:
🟤  ==> """+str(c1)+"""
🟣  ==> """+str(c2)+"""
🟡  ==> """+str(c3)+"""
🔵  ==> """+str(c4)+"""
Possible amount : """+f'{total:.3f} BCoin'+"""
"""

    logger(report, telegram=True)

def sendBCoinReport():
    if telegram_data['telegram_mode'] == False:
        return
    if(len(telegram_data["telegram_chat_id"]) <= 0 or telegram_data["enable_coin_report"] is False):
        return

    clickBtn(chest_button)

    sleep(5, 15)

    coin = positions(coin_icon, return_0=True)
    if len(coin) > 0:
        x, y, w, h = coin[0]

        with mss.mss() as sct:
            sct_img = np.array(sct.grab(sct.monitors[c['monitor_to_use']]))
            crop_img = sct_img[y:y+h, x:x+w]
            cv2.imwrite('bcoin-report.%s' % telegram_data["format_of_images"], crop_img)
            time.sleep(1)
            try:
                for chat_id in telegram_data["telegram_chat_id"]:
                    # TBot.send_document(chat_id=chat_id, document=open('bcoin-report.png', 'rb'))
                    TBot.send_photo(chat_id=chat_id, photo=open('bcoin-report.%s' % telegram_data["format_of_images"], 'rb'))
            except:
                logger("Telegram offline...")
    clickBtn(x_button_img)
    logger("BCoin Report sent.", telegram=True)

def sendMapReport():
    if telegram_data['telegram_mode'] == False:
        return
    if(len(telegram_data["telegram_chat_id"]) <= 0 or telegram_data["enable_map_report"] is False):
        return

    back = positions(arrow_img)
    full_screen = positions(full_screen_img)
    if len(back) <= 0 or len(full_screen) <= 0:
        return
    x, y, _, _ = back[0]
    x1, y1, w, h = full_screen[0]
    newY0 = y
    newY1 = y1
    newX0 = x
    newX1 = x1 + w

    with mss.mss() as sct:
        sct_img = np.array(sct.grab(sct.monitors[c['monitor_to_use']]))
        crop_img = sct_img[newY0:newY1, newX0:newX1]
        # resized = cv2.resize(crop_img, (500, 250))

        cv2.imwrite('map-report.%s' % telegram_data["format_of_images"], crop_img)
        time.sleep(1)
        try:
            for chat_id in telegram_data["telegram_chat_id"]:
                # TBot.send_document(chat_id=chat_id, document=open('map-report.png', 'rb'))
                TBot.send_photo(chat_id=chat_id, photo=open('map-report.%s' % telegram_data["format_of_images"], 'rb'))
        except:
            logger("Telegram offline...")

        try:
            sendPossibleAmountReport(sct_img[:,:,:3])
        except:
            logger("Error finding chests.")

    clickBtn(x_button_img)
    logger("Map Report sent.", telegram=True)

def logger(message, telegram=False):
    datetime = time.localtime()
    formatted_datetime = time.strftime("%d/%m/%Y %H:%M:%S", datetime)

    formatted_message = "[{}] => {}".format(formatted_datetime, message)

    print(formatted_message)

    if telegram == True:
        sendTelegramMessage(formatted_message)

    if (c['save_log_to_file'] == True):
        logger_file = open("logger.log", "a", encoding='utf-8')
        logger_file.write(formatted_message + '\n')
        logger_file.close()

    return True

def clickBtn(img,name=None, timeout=3, threshold = ct['default']):
    if not name is None:
        pass
    start = time.time()
    clicked = False
    while(not clicked):
        matches = positions(img, threshold=threshold)
        if(matches is False):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass
                    # print('timed out')
                return False
            # print('button not found yet')
            continue

        x,y,w,h = matches[0]
        # pyautogui.moveTo(x+(w/2),y+(h/2),1)
        # pyautogui.moveTo(int(random.uniform(x, x+w)),int(random.uniform(y, y+h)),1)
        hc.move((int(random.uniform(x, x+w)), int(random.uniform(y, y+h))),1)
        pyautogui.click()
        return True

def printScreen():
    with mss.mss() as sct:
        # The screen part to capture
        # Grab the data
        sct_img = np.array(sct.grab(sct.monitors[c['monitor_to_use']]))
        return sct_img[:,:,:3]

def positions(target, threshold=ct['default'], base_img=None, return_0=False):
    if base_img is None:
        img = printScreen()
    else:
        img = base_img

    w = target.shape[1]
    h = target.shape[0]

    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    if return_0 is False:
        if len(rectangles) > 0:
            # sys.stdout.write("\nGet_coords. " + str(rectangles) + " " + str(weights) + " " + str(w) + " " + str(h) + " ")
            return rectangles
        else:
            return False
    else:
        return rectangles

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
        # print('threshold = %.3f' % threshold)
        return findPuzzlePieces(result, piece_img,threshold-0.01)

    if len(r) == 2:
        # print('match')
        return r

    if len(r) > 2:
        logger('overshoot by %d' % len(r))

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

def show(rectangles = None, img = None):

    if img is None:
        with mss.mss() as sct:
            img = np.array(sct.grab(sct.monitors[c['monitor_to_use']]))

    if rectangles is not None:
        for (x, y, w, h) in rectangles:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)

def getPiecesPosition(t = 150):
    popup_pos = positions(robot)
    if popup_pos is False:
        logger('puzzle not found')
        return
    rx, ry, _, _ = popup_pos[0]

    w = 380
    h = 200
    x_offset = -40
    y_offset = 65

    y = ry + y_offset
    x = rx + x_offset

    img = printScreen()
    #TODO tirar um poco de cima

    cropped = img[ y : y + h , x: x + w]
    blurred = cv2.GaussianBlur(cropped, (3, 3), 0)
    edges = cv2.Canny(blurred, threshold1=t/2, threshold2=t,L2gradient=True)
    # img = cv2.Laplacian(img,cv2.CV_64F)

    # gray_piece_img = cv2.cvtColor(piece, cv2.COLOR_BGR2GRAY)
    piece_img = cv2.cvtColor(piece, cv2.COLOR_BGR2GRAY)
    # print('----')
    # print(piece_img.shape)
    # print(edges.shape)
    # print('----')
    # piece_img = cv2.Canny(gray_piece_img, threshold1=t/2, threshold2=t,L2gradient=True)
    # result = cv2.matchTemplate(edges,piece_img,cv2.TM_CCOEFF_NORMED)
    result = cv2.matchTemplate(edges,piece_img,cv2.TM_CCORR_NORMED)

    puzzle_pieces = findPuzzlePieces(result, piece_img)

    if puzzle_pieces is None:
        return

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
    slider_pos = positions(slider, return_0=True)
    if len (slider_pos) == 0:
        return False
    x, y, w, h = slider_pos[0]
    position = [x+w/2,y+h/2]
    return position

def check_puzzle():
    puzzle_pos = positions(robot)
    if puzzle_pos is not False:
        solveCaptcha()
    else:
        return True

def solveCaptcha():
    pieces_start_pos = getPiecesPosition()
    if pieces_start_pos is False:
        return
    slider_start_pos = getSliderPosition()
    if slider_start_pos is False:
        return

    x,y = slider_start_pos
    # pyautogui.moveTo(x,y,1)
    hc.move((int(x),int(y)), np.random.randint(1,2))
    pyautogui.mouseDown()
    # pyautogui.moveTo(x+300 ,y,0.5)
    hc.move((int(x + 350),int(y)), np.random.randint(1,2))
    pieces_end_pos = getPiecesPosition()


    piece_start, _, _, _ = getLeftPiece(pieces_start_pos)
    piece_end, _, _, _ = getRightPiece(pieces_end_pos)
    piece_middle, _, _, _  = getRightPiece(pieces_start_pos)
    slider_start, _, = slider_start_pos
    slider_end, _ = getSliderPosition()
    # print (piece_start)
    # print (piece_end)
    # print (piece_middle)
    # print (slider_start)
    # print (slider_end)

    piece_domain = piece_end - piece_start
    middle_piece_in_percent = (piece_middle - piece_start)/piece_domain
    # print('middle_piece_in_percent{} '.format(middle_piece_in_percent ))

    slider_domain = slider_end - slider_start
    slider_awnser = slider_start + (middle_piece_in_percent * slider_domain)
    # arr = np.array([[int(piece_start),int(y-20),int(10),int(10)],[int(piece_middle),int(y-20),int(10),int(10)],[int(piece_end-20),int(y),int(10),int(10)],[int(slider_awnser),int(y),int(20),int(20)]])

    # pyautogui.moveTo(slider_awnser,y,0.5)
    hc.move((int(slider_awnser),int(y)), np.random.randint(1,2))
    time.sleep(1)
    pyautogui.mouseUp()
    time.sleep(2)


    puzzle_pos = positions(robot)
    if puzzle_pos is not False:
        logger('puzzle error')
        solveCaptcha()
    else:
        logger('puzzle solved')

    # show(arr)

def scroll():

    # width, height = pyautogui.size()
    # pyautogui.moveTo(width/2-200, height/2,1)
    character_indicator_pos = positions(character_indicator)
    if character_indicator_pos is False:
        return

    x, y, w, h = character_indicator_pos[0]
    hc.move((int(x+(w/2)),int(y+h+offsets['character_indicator'])), np.random.randint(1,2))

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.click()
        pyautogui.scroll(-c['scroll_size'])
    else:
        # pyautogui.dragRel(0,-c['click_and_drag_amount'],duration=1, button='left')
        pyautogui.mouseDown(button='left')
        hc.move((int(x),int(y+(-c['click_and_drag_amount']))), np.random.randint(1,2))
        pyautogui.mouseUp(button='left')

def clickButtons():
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])

    if c['debug'] is not False:
        logger('%d buttons detected' % len(buttons))

    if buttons is False:
        return False
    for (x, y, w, h) in buttons:
        # pyautogui.moveTo(x+(w/2),y+(h/2),1)
        hc.move((int(x+(w/2)),int(y+(h/2))), np.random.randint(1,2))
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 15:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold', telegram=True)
            return
    logger('Clicking in %d heroes detected.' % len(buttons), telegram=True)
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
    offset = offsets['work_button']
    green_bars = positions(green_bar, threshold=ct['green_bar'])
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'], return_0=True)

    if c['debug'] is not False:
        logger('%d green bars detected' % len(green_bars))
        logger('%d buttons detected' % len(buttons))

    not_working_green_bars = []
    if green_bars is False:
        return False
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('Clicking in %d heroes with green bar detected.' % len(not_working_green_bars), telegram=True)

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        # pyautogui.moveTo(x+offset+(w/2),y+(h/2),1)
        hc.move((int(x+offset+(w/2)),int(y+(h/2))), np.random.randint(1,2))
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        if hero_clicks > 15:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold', telegram=True)
            return
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)

def clickFullBarButtons():
    offset = offsets['work_button_full']
    full_bars = positions(full_stamina, threshold=ct['default'])
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'], return_0=True)

    if c['debug'] is not False:
        logger('%d FULL bars detected' % len(full_bars))
        logger('%d buttons detected' % len(buttons))

    not_working_full_bars = []
    if full_bars is False:
        return False
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        logger('Clicking in %d heroes with FULL bar detected.' % len(not_working_full_bars), telegram=True)

    for (x, y, w, h) in not_working_full_bars:
        # pyautogui.moveTo(x+offset+(w/2),y+(h/2),1)
        hc.move((int(x+offset+(w/2)),int(y+(h/2))), np.random.randint(1,2))
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        if hero_clicks > 15:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold', telegram=True)
            return

    return len(not_working_full_bars)

def current_screen():
    if positions(arrow_img) is not False:
        # sys.stdout.write("\nThunt. ")
        return "thunt"
    elif positions(teasureHunt_icon_img) is not False:
        # sys.stdout.write("\nmain. ")
        return "main"
    elif positions(connect_wallet_btn_img) is not False:
        # sys.stdout.write("\nlogin. ")
        return "login"
    elif positions(character_indicator) is not False:
        # sys.stdout.write("\ncharacter. ")
        return "character"
    else:
        # sys.stdout.write("\nUnknown. ")
        return "unknown"

def goToHeroes():
    if current_screen() == "thunt":
        if clickBtn(arrow_img):
            sleep(1, 3)
            if clickBtn(hero_img):
                sleep(1, 3)
                check_puzzle()
                waitForImg(home_img)
    if current_screen() == "main":
        if clickBtn(hero_img):
            sleep(1, 3)
            check_puzzle()
            waitForImg(home_img)
    if current_screen() == "unknown" or current_screen() == "login":
        check_for_logout()

def goToGame():
    if current_screen() == "main":
        clickBtn(teasureHunt_icon_img)
    if current_screen() == "character":
        if clickBtn(x_button_img):
            sleep(1, 3)
            clickBtn(teasureHunt_icon_img)
    if current_screen() == "unknown" or current_screen() == "login":
        check_for_logout()

def refreshHeroesPositions():
    logger("Refreshing heroes Positions.")
    if current_screen() == "thunt":
        if clickBtn(arrow_img):
            time.sleep(5)
    if current_screen() == "main":
        if clickBtn(teasureHunt_icon_img):
            return True
        else:
            return False
    else:
        return False

def login():
    global login_attempts

    randomMouseMovement()

    if clickBtn(connect_wallet_btn_img):
        logger('Connect wallet button detected, logging in!')
        time.sleep(2)
        solveCaptcha()
        waitForImg((sign_btn_img, metamask_unlock_img), multiple=True)

    metamask_unlock_coord = positions(metamask_unlock_img)
    if metamask_unlock_coord is not False:
        if(metamask_data["enable_login_metamask"] is False):
            logger("Metamask Locked! But login with password is disabled. Exiting.")
            exit()
        logger("Found unlock button. Waiting for password")
        password = metamask_data["password"]
        pyautogui.typewrite(password, interval=0.1)
        sleep(1, 3)
        if clickBtn(metamask_unlock_img):
            logger("Unlock button clicked")

    if clickBtn(sign_btn_img):
        logger("Found sign button. Waiting to check if logged in.")
        time.sleep(5)
        if clickBtn(sign_btn_img): ## twice because metamask glitch
            logger("Found glitched sign button. Waiting to check if logged in.")
        # time.sleep(25)
        waitForImg(teasureHunt_icon_img, timeout=60)

    if current_screen() == "main":
        logger("Logged in.", telegram=True)
        return True
    else:
        logger("Login failed. Trying again.")
        login_attempts += 1

        if (login_attempts > 3):
            logger(">3 login attempts. Retrying.", telegram=True)
            pyautogui.hotkey('ctrl', 'f5')
            login_attempts = 0

            if clickBtn(metamask_cancel_button):
                logger("Metamask is glitched. Fixing.")
            
            waitForImg(connect_wallet_btn_img)

        login()

    handle_error()

def handle_error():
    if positions(error_img, ct['error']) is not False:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        logger("Error detected. Trying to resolve.", telegram=True)
    else:
        return False

    if clickBtn(ok_btn_img):
        logger("Refreshing page.")
        pyautogui.hotkey('ctrl', 'f5')
        waitForImg(connect_wallet_btn_img)
        login()

def refreshHeroes():
    goToHeroes()

    if c['select_heroes_mode'] == "full":
        logger("Sending heroes with full stamina bar to work!")
    elif c['select_heroes_mode'] == "green":
        logger("Sending heroes with green stamina bar to work!")
    else:
        logger("Sending all heroes to work!")

    buttonsClicked = 0
    empty_scrolls_attempts = c['scroll_attempts']

    while(empty_scrolls_attempts > 0):
        if c['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons()
        elif c['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked = clickButtons()

        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        sleep(1, 3)
    logger('{} total heroes sent since the bot started'.format(hero_clicks), telegram=True)
    goToGame()

def check_for_logout():
    if current_screen() == "unknown" or current_screen() == "login":
        if positions(connect_wallet_btn_img) is not False:
            logger("Logout detected.", telegram=True)
            logger("Refreshing page.", telegram=True)
            pyautogui.hotkey('ctrl', 'f5')
            waitForImg(connect_wallet_btn_img)
            login()
        elif positions(sign_btn_img):
            logger("Sing button detected.", telegram=True)
            if clickBtn(metamask_cancel_button):
                logger("Metamask is glitched. Fixing.", telegram=True)
        else:
            return False
            
    else:
        return False

def waitForImg(imgs, timeout=30, threshold=0.5, multiple=False):
    start = time.time()
    while True:
        if multiple is not False:
            for img in imgs:
                matches = positions(img, threshold=threshold)
                if matches is False:
                    hast_timed_out = time.time()-start > timeout
                    if hast_timed_out is not False:
                        return False
                    continue
                return True
        else:
            matches = positions(imgs, threshold=threshold)
            if matches is False:
                hast_timed_out = time.time()-start > timeout
                if hast_timed_out is not False:
                    return False
                continue
            return True

def sleep(min, max):
	sleep = random.uniform(min,max)
	randomMouseMovement()
	return time.sleep(sleep)

def randomMouseMovement():
    x, y = pyautogui.size()
    x = np.random.randint(0, x)
    y = np.random.randint(0, y)
    hc.move((int(x), int(y)), np.random.randint(1,3))

def main():
    print('version: ' + c['version'])
    if version > c['version']:
        logger('New version available. Please update.', telegram=True)
    input("Press Enter to start...")
    logger("Starting bot...", telegram=True)

    t = c['time_intervals']

    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    "refresh_heroes" : 0
    }

    while True:
        if current_screen() == "login":
            login()
        
        handle_error()

        check_puzzle()

        now = time.time()

        if now - last["heroes"] > t['send_heroes_for_work'] * 60:
            last["heroes"] = now + (random.randint(0, t['send_heroes_for_work_variable']) * 60)
            last["refresh_heroes"] = now
            logger('Sending heroes to work.', telegram=True)
            refreshHeroes()

        if current_screen() == "main":
            if clickBtn(teasureHunt_icon_img):
                logger("Entering treasure hunt")
                last["refresh_heroes"] = now

        if current_screen() == "thunt":
            if clickBtn(new_map_btn_img):
                logger("New map!")
                last["new_map"] = now
                sleep(1, 2)
                check_puzzle()
                sleep(2, 3)
                sendMapReport()
                sleep(3, 5)
                sendBCoinReport()
                
        if current_screen() == "character":
            clickBtn(x_button_img)
            sleep(1, 3)

        if now - last["refresh_heroes"] > t['refresh_heroes_positions'] * 60 :
            last["refresh_heroes"] = now + (random.randint(0, t['refresh_heroes_positions_variable']) * 60)
            logger('Refreshing Heroes Positions.')
            refreshHeroesPositions()

        check_for_logout()
        sys.stdout.flush()
        time.sleep(general_check_time)


main()