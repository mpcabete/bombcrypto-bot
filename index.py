from cv2 import cv2
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
ct = c['threshold']

pyautogui.PAUSE = c['time_intervals']['interval_between_moviments']

pyautogui.FAILSAFE = True
hero_clicks = 0
login_attempts = 0
last_log_is_progress = False







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
green_bar = cv2.imread('targets/green-bar.png')
full_stamina = cv2.imread('targets/full-stamina.png')
puzzle_img = cv2.imread('targets/puzzle.png')
piece = cv2.imread('targets/piece.png')
robot = cv2.imread('targets/robot.png')
slider = cv2.imread('targets/slider.png')


###################### puzzle #############
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
        print('threshold = %.3f' % threshold)
        return findPuzzlePieces(result, piece_img,threshold-0.01)

    if len(r) == 2:
        print('match')
        return r

    if len(r) > 2:
        print('overshoot by %d' % len(r))

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
        print('puzzle not found')
        return
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
    print('----')
    print(piece_img.shape)
    print(edges.shape)
    print('----')
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
    slider_pos = positions(slider)
    if len (slider_pos) == 0:
        return False
    x, y, w, h = slider_pos[0]
    position = [x+w/2,y+h/2]
    return position

def solveCapcha():
    logger('checking for capcha')
    pieces_start_pos = getPiecesPosition()
    if pieces_start_pos is None :
        return
    slider_start_pos = getSliderPosition()

    x,y = slider_start_pos
    pyautogui.moveTo(x,y,1)
    pyautogui.mouseDown()
    pyautogui.moveTo(x+300 ,y,0.5)
    pieces_end_pos = getPiecesPosition()


    piece_start, _, _, _ = getLeftPiece(pieces_start_pos)
    piece_end, _, _, _ = getRightPiece(pieces_end_pos)
    piece_middle, _, _, _  = getRightPiece(pieces_start_pos)
    slider_start, _, = slider_start_pos
    slider_end, _ = getSliderPosition()
    print (piece_start)
    print (piece_end)
    print (piece_middle)
    print (slider_start)
    print (slider_end)

    piece_domain = piece_end - piece_start
    middle_piece_in_percent = (piece_middle - piece_start)/piece_domain
    print('middle_piece_in_percent{} '.format(middle_piece_in_percent ))

    slider_domain = slider_end - slider_start
    slider_awnser = slider_start + (middle_piece_in_percent * slider_domain)
    # arr = np.array([[int(piece_start),int(y-20),int(10),int(10)],[int(piece_middle),int(y-20),int(10),int(10)],[int(piece_end-20),int(y),int(10),int(10)],[int(slider_awnser),int(y),int(20),int(20)]])

    pyautogui.moveTo(slider_awnser,y,0.5)
    pyautogui.mouseUp()

    # show(arr)
    #########################################

def logger(message, progress_indicator = False):
    global last_log_is_progress



    # Start progress indicator and append dots to in subsequent progress calls
    if progress_indicator:
        if not last_log_is_progress:
            last_log_is_progress = True
            sys.stdout.write('\n => .')
            sys.stdout.flush()
        else:
            sys.stdout.write('.')
            sys.stdout.flush()

        return

    if last_log_is_progress:
        sys.stdout.write('\n\n')
        sys.stdout.flush()
        last_log_is_progress = False



    datetime = time.localtime()
    formatted_datetime = time.strftime("%d/%m/%Y %H:%M:%S", datetime)

    formatted_message = "[{}] \n => {} \n\n".format(formatted_datetime, message)


    print(formatted_message)

    if (c['save_log_to_file'] == True):
        logger_file = open("logger.log", "a")
        logger_file.write(formatted_message)
        logger_file.close()

    return True

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
        pyautogui.moveTo(x+w/2,y+h/2,1)
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

def positions(target, threshold=ct['default']):
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

    commoms = positions(commom_img, threshold = ct['commom'])
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
        pyautogui.dragRel(0,-c['click_and_drag_amount'],duration=1, button='left')


def clickButtons():
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        pyautogui.moveTo(x+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
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
    green_bars = positions(green_bar, threshold=ct['green_bar'])
    logger('%d green bars detected' % len(green_bars))
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])
    logger('%d buttons detected' % len(buttons))

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('%d buttons with green bar detected' % len(not_working_green_bars))
        logger('Clicking in %d heroes.' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        pyautogui.moveTo(x+offset+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        if hero_clicks > 20:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)

def clickFullBarButtons():
    offset = 100
    full_bars = positions(full_stamina, threshold=ct['default'])
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        logger('Clicking in %d heroes.' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        pyautogui.moveTo(x+offset+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1

    return len(not_working_full_bars)

def goToHeroes():
    if clickBtn(arrow_img):
        global login_attempts
        login_attempts = 0

    solveCapcha()
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
        logger('Too many login attempts, refreshing.')
        login_attempts = 0
        pyautogui.hotkey('ctrl','f5')
        return

    if clickBtn(connect_wallet_btn_img, name='connectWalletBtn', timeout = 10):
        solveCapcha()
        login_attempts = login_attempts + 1
        logger('Connect wallet button detected, logging in!')
        #TODO mto ele da erro e poco o botao n abre
        # time.sleep(10)

    if clickBtn(sign_btn_img, name='sign button', timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        # time.sleep(5)
        if clickBtn(teasureHunt_icon_img, name='teasureHunt', timeout = 15):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)
        return
        # click ok button

    if not clickBtn(select_metamask_no_hover_img, name='selectMetamaskBtn'):
        if clickBtn(select_wallet_hover_img, name='selectMetamaskHoverBtn', threshold = ct['select_wallet_buttons'] ):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo 
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)
    else:
        pass
        # print('sleep in case there is no metamask text removed')
        # time.sleep(20)

    if clickBtn(sign_btn_img, name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        # time.sleep(25)
        if clickBtn(teasureHunt_icon_img, name='teasureHunt', timeout=25):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)

    if clickBtn(ok_btn_img, name='okBtn', timeout=5):
        pass
        # time.sleep(15)
        # print('ok button clicked')




def refreshHeroes():
    goToHeroes()

    if c['select_heroes_mode'] == "full":
        logger("Sending heroes with full stamina bar to work!")
    elif c['select_heroes_mode'] == "green":
        logger("Sending heroes with green stamina bar to work!")
    else:
        logger("Sending all heroes to work!")

    buttonsClicked = 1
    empty_scrolls_attempts = c['scroll_attemps']

    while(empty_scrolls_attempts >0):
        if c['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons()
        elif c['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked = clickButtons()

        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        time.sleep(2)
    logger('{} heroes sent to work so far'.format(hero_clicks))
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
            logger('Sending heroes to work.')
            refreshHeroes()

        if now - last["login"] > t['check_for_login'] * 60:
            logger("Checking if game has disconnected.")
            sys.stdout.flush()
            last["login"] = now
            login()

        if now - last["new_map"] > t['check_for_new_map_button']:
            last["new_map"] = now
            if clickBtn(new_map_btn_img):
                with open('new-map.log','a') as new_map_log:
                    new_map_log.write(str(time.time())+'\n')
                logger('New Map button clicked!')

        if now - last["refresh_heroes"] > t['refresh_heroes_positions'] * 60 :
            solveCapcha()
            last["refresh_heroes"] = now
            logger('Refreshing Heroes Positions.')
            refreshHeroesPositions()

        #clickBtn(teasureHunt)
        logger(None, progress_indicator=True)

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
# pip uninstall opencv-python

# pip install --upgrade opencv-python==4.5.3.56
