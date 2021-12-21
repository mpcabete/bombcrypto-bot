from cv2 import cv2
import numpy as np
import mss
import pyautogui
import time
import sys
import yaml
import random
import statistics
from telebot import TeleBot



if __name__ == '__main__':

    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)
ct = c['threshold']
pyautogui.PAUSE = c['time_intervals']['interval_between_moviments']

pyautogui.FAILSAFE = True
hero_clicks = 0
login_attempts = 0
error_screen = 0
bot = TeleBot("1036756397:AAHBJclvJdADKAqwEtpk7EylXHeeXavMA3A")

my_telegram = 26917503
notify = 0

go_work_img = cv2.imread('targets/go-work.png')
upgrade = cv2.imread('targets/upgrade.png')
commom_img = cv2.imread('targets/commom-text.png')
arrow_img = cv2.imread('targets/go-back-arrow.png')
hero_img = cv2.imread('targets/hero-icon.png')
x_button_img = cv2.imread('targets/x.png')
teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
ok_btn_img = cv2.imread('targets/ok.png')
connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
select_wallet_hover_img = cv2.imread('targets/select-wallet-2-hover.png')
select_metamask_no_hover_img = cv2.imread('targets/select-wallet-1-no-hover.png')
sign_btn_img = cv2.imread('targets/select-wallet-2.png')
metamask_pending = cv2.imread('targets/metamask1.png')
metamask_cancel= cv2.imread('targets/cancel.png')
bombcrypto_logo = cv2.imread('targets/bombcrypto.png')
new_map_btn_img = cv2.imread('targets/new-map.png')
green_bar = cv2.imread('targets/green-bar.png')
expand_btn = cv2.imread('targets/expand_button.png')
challange_top_img = cv2.imread('targets/slide.png')
robot_img = cv2.imread('targets/robot.png')

def dot():
    sys.stdout.write(".")
    sys.stdout.flush()

def clickBtn(img,name=None, timeout=3, threshold = ct['default']):
    dot()
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
        pyautogui.moveTo(x+w/2,y+h/2,1,pyautogui.easeOutQuad)
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

    commoms = positions(commom_img, threshold = ct['common'])
    if (len(commoms) == 0):
        # print('no commom text found')
        return
    x,y,w,h = commoms[len(commoms)-1]
    # print('moving to {},{} and scrolling'.format(x,y))
#
    pyautogui.moveTo(x,y,1,pyautogui.easeOutQuad)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0,-c['click_and_drag_amount'],duration=1)


def clickButtons():
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        pyautogui.moveTo(x+(w/2),y+(h/2),1,pyautogui.easeOutQuad)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        print(f"{x} {y} {w} {h}")
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
    buttons = positions(go_work_img, threshold=ct['go_to_work_btn'])

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        sys.stdout.write('\nclicking in %d heroes.' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        pyautogui.moveTo(x+offset+(w/2),y+(h/2),1,pyautogui.easeOutQuad)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)

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

def solveChallenge():
    color = (125,125,125)
    color_slider = (251,220,45)
    color_peca = (0,0,0)
    color_slider_field = (130,85,64)
    telaChallenge = pyautogui.screenshot()
    horizontal = []
    slider_horizontal = []
    slider_vertical = []
    peca_horizontal = []
    field_horizontal = []
    field_vertical = []
    piece_travel = 300
    acceleration = 0.0
    sys.stdout.write('\nSolving captcha\n')
    try:
        for x in range(770,845):
            for y in range(430,625):
               if telaChallenge.getpixel((x, y)) == color_peca:
                   peca_horizontal.append(x)
        peca_mean = int(statistics.mean(peca_horizontal))
        #print(f"Peça: {peca_mean}")
    except:
        sys.stdout.write("\nError finding piece\n")
        return False
    try:
        for x in range(775,1160):
            for y in range(640,680):
               if telaChallenge.getpixel((x, y)) == color_slider_field:
                   field_horizontal.append(x)
                   field_vertical.append(y)
        fieldx = max(field_horizontal)-10
        fieldy = max(field_vertical)
        #print(f"Field: ({fieldx},{fieldy})")
    except:
        sys.stdout.write("\nError finding slider field\n")
        return False
    try:
        for x in range(775,1000):
            for y in range(640,680):
               if telaChallenge.getpixel((x, y)) == color_slider:
                   slider_horizontal.append(x)
                   slider_vertical.append(y)
        minfieldx = min(slider_horizontal)
        sliderx = int(statistics.mean(slider_horizontal))
        slidery = int(statistics.mean(slider_vertical))
        #print(f"Slider: ({sliderx},{slidery}, Min slider: {minfieldx})")
    except:
        sys.stdout.write("\nError finding slider\n")
        return False
    try:
        for x in range(850,1070):
            for y in range(430,586):
               if telaChallenge.getpixel((x, y)) == color:
                   horizontal.append(x)
        challenge_mean = statistics.mean(horizontal)
        #print(f"Challenge: ({challenge_mean})")
    except:
        sys.stdout.write("\nError finding challenge\n")
        return False
    try:
        if len(slider_horizontal) == 0:
            sys.stdout.write("\nCouldn't find slider\n")
            return False
        pyautogui.moveTo(sliderx, slidery, 1, pyautogui.easeOutQuad)

        if fieldx - sliderx < 200:
            if challenge_mean > 960:
                challenge_drag = challenge_mean * 0.99
            else:
                challenge_drag = challenge_mean * 1.01
        else:
            challenge_drag = challenge_mean
        #print(f"Challenge Drag {challenge_drag}")
        moveTime = random.randint(100,200)/100
        pyautogui.mouseDown()
        pyautogui.moveTo(challenge_drag, fieldy, moveTime, pyautogui.easeOutQuad)
        pyautogui.mouseUp()
        return True
    except:
        sys.stdout.write("\nError sliding challenge\n")
        return False

def captcha():
    time.sleep(1)
    tentativas = 0
    sliderx, slidery = get_object_by_color(775,1000,640,680,(251,220,45),"slider")
    print(len(sliderx),len(slidery))
    if len(sliderx) > 150 and len(slidery) > 150:
        captcha = True
    else:
        captcha = False
        sys.stdout.write('\nNo captcha found\n')
        return True
    while captcha:
        sys.stdout.write('\nCaptcha Found\n')
        result = solveChallenge()
        tentativas += 1
        sliderx, slidery = get_object_by_color(775, 1000, 640, 680, (251, 220, 45), "slider")
        print(len(sliderx), len(slidery))
        if len(sliderx) < 150 and len(slidery) < 150:
            captcha = False
            sys.stdout.write('\nNo more captcha found\n')
            return True
        if tentativas > 3:
            sys.stdout.write('\nToo many tries\n')
            pyautogui.hotkey('ctrl', 'f5')
            return False



def goToHeroes():
    heroScreen = smartMove(upgrade, justcheck=True)
    if heroScreen:
        return True
    elif clickBtn(arrow_img):
        global login_attempts
        login_attempts = 0
        robotCheck = captcha()
        if not robotCheck:
            return False
    # time.sleep(5)
    hero = clickBtn(hero_img)
    robotCheck = captcha()
    if not robotCheck:
        return False
    return hero
    # time.sleep(5)


def goToGame():
    # in case of server overload popup
    try:
        clickBtn(x_button_img)
        robotCheck = captcha()
        if not robotCheck:
            return False
        # time.sleep(3)
        clickBtn(x_button_img)
        robotCheck = captcha()
        if not robotCheck:
            return False
        clickBtn(teasureHunt_icon_img)
        robotCheck = captcha()
        if not robotCheck:
            return False
        return True
    except:
       sys.stdout.write("\nError going to Game\n")
       return False



def refreshHeroesPositions():
    sys.stdout.write("\nClick arow\n")
    clickBtn(arrow_img)
    robotCheck = captcha()
    if not robotCheck:
        return False
    sys.stdout.write("\nClick teasure\n")
    clickBtn(teasureHunt_icon_img)
    robotCheck = captcha()
    if not robotCheck:
        return False
    # time.sleep(3)
    sys.stdout.write("\nClick teasure again\n")
    clickBtn(teasureHunt_icon_img)
    robotCheck = captcha()
    if not robotCheck:
        return False
    return True


def checkConnection():
    global notify
    global my_telegram
    connectWalletBtnScreen = checkScreen(connect_wallet_btn_img,confidence=ct['connect_Wallet_button'])
    treasureBtnScreen = checkScreen(teasureHunt_icon_img)
    okBtnScreen = checkScreen(ok_btn_img)
    expandScr = matchPixel(1420,860,(64, 173, 211))
    captchaScrx, captchaScry = get_object_by_color(775, 1160, 640, 680, (251, 220, 45), "slider")
    if len(captchaScrx) > 250 and len(captchaScry) > 250:
        sys.stdout.write('\nChalenge found at connection check\n')
        solve = solveChallenge()
        if solve:
            sys.stdout.write('\nChalenge solved\n')
            pass
        else:
            sys.stdout.write("\nCouldn't solve challenge at connection check, refreshing\n")
            pyautogui.hotkey('ctrl', 'f5')
            return False
    elif treasureBtnScreen:
        sys.stdout.write('\nTreasure button found!')
        return True
    elif walletSelectionScreen:
        sys.stdout.write('\nWallet selection screen found, refreshing!')
        pyautogui.hotkey('ctrl','f5')
        time.sleep(5)
        return False
    elif connectWalletBtnScreen:
        sys.stdout.write('\nConnect wallet button detected, logging in!')
        connected = login()
        return connected
    elif okBtnScreen:
        sys.stdout.write('\nPressing Ok\n')
        clickBtn(ok_btn_img, name='okBtn', timeout=5)
        time.sleep(15)
        connected = login()
        return connected
    elif not expandScr:
        notify = notify + 1
        sys.stdout.write('\nWindow not found\n')
        if notify > 180:
            bot.send_message(my_telegram,"Verificar jogo",disable_notification=True) 
            notify = 0
        time.sleep(60)
        return False
    else:
        sys.stdout.write('\nFound nothing else\n')
        return True


def login():
    global login_attempts
    
    if login_attempts > 3:
        sys.stdout.write('\nToo many login attempts, refreshing.\n')
        login_attempts = 0
        pyautogui.hotkey('ctrl','f5')
        return False
    
    if clickBtn(metamask_pending, name='metamask_pending_button', timeout = 2, threshold = 1):
        sys.stdout.write('\Metamask peding login found')
        try: 
            clickBtn(metamask_cancel, name='metamask_cancel_button', timeout = 2)
            clickBtn(bombcrypto_logo, name='bombcrypto_blank_area', timeout = 2)
            pyautogui.hotkey('ctrl','f5')
            time.wait(4)
        except:
            login_attempts = login_attempts + 1
       
    connectWalletBtnScreen = checkScreen(connect_wallet_btn_img,confidence=ct['connect_Wallet_button'])
    if connectWalletBtnScreen:
        try:
            login_attempts = login_attempts + 1
            time.sleep(1)
            walletx, wallety = connectWalletBtnScreen
            pyautogui.moveTo(walletx, wallety,1,pyautogui.easeOutQuad)
            pyautogui.click()
            sys.stdout.write('\nConnect wallet button pressed\n')
        except:
            sys.stdout.write('\nError clicking on wallet button\n')
            login_attempts = 4 #Probla
            return False
    selectMetamask = smartMove(select_wallet_hover_img,confidence=ct['select_wallet_buttons'])

    robotCheck = captcha()
    if not robotCheck:
        return False

    if clickBtn(sign_btn_img, name='signBtn', timeout = 40):
        sys.stdout.write('\nSign-In button detected, logging in!')
        login_attempts = login_attempts + 1
        time.sleep(ct['game_load_time'])
        if clickBtn(ok_btn_img, name='okBtn', timeout=5):
            login_attempts = login_attempts + 1
            return False
        elif clickBtn(teasureHunt_icon_img, name='teasureHunt', timeout=10):
            login_attempts = 0
            return True
        else: 
            login_attempts = login_attempts + 1
            return False
    else:
        login_attempts = login_attempts + 1
        return False

           
        # time.sleep(15)



def refreshHeroes():
    heroscreen = goToHeroes()
    global error_screen
    if not heroscreen:
         error_screen = error_screen + 1
         return "Error going to hero screen"
    if c['only_click_heroes_with_green_bar']:
        print('\nSending heroes with an green stamina bar to work!\n')
    else:
        sys.stdout.write('\nSending all heroes to work!\n')
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
    gtgame = goToGame()
    if gtgame:
        return "Refresh Success"
        error_screen = 0
    else:
        return "Refresh Error"

def main():
    time.sleep(5)
    t = c['time_intervals']

    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    "refresh_heroes" : 0,
    "captcha": 0
    }
    global error_screen

    while True:
        now = time.time()
        if now - last["login"] > t['check_for_login'] * 60:
            connected = checkConnection()
            if connected:
                sys.stdout.write(f"""\nConnected - {time.strftime("%H:%M:%S")}\n""")
                last["login"] = now
        while not connected:
            sys.stdout.write("\nGame is not running.\n")
            sys.stdout.flush()
            last["login"] = now
            connected = checkConnection()
            if connected:
                sys.stdout.write("\nConnected successfully.\n")
            else:
                sys.stdout.write("\n Couldn't connect. Trying again in 15 seconds\n")
                time.sleep(10)
        while connected:
            now = time.time()
            if now - last["login"] > t['check_for_login'] * 60:
                connected = checkConnection()
                if connected:
                    sys.stdout.write(f"""\nConnected - {time.strftime("%H:%M:%S")}""")
                    last["login"] = now

            if now - last["heroes"] > t['send_heroes_for_work']:
                last["heroes"] = now
                sys.stdout.write('\nSending heroes to work.\n')
                result = refreshHeroes()
                sys.stdout.write(f"\n{result}\n")

            if error_screen > 3:
                sys.stdout.write("\n Errors sending heroes to work. Time to refresh.\n")
                pyautogui.hotkey('ctrl', 'f5')
                error_screen = 0
                connected = False

            if now - last["new_map"] > t['check_for_new_map_button'] * 60:
                last["new_map"] = now
                if clickBtn(new_map_btn_img):
                    with open('new-map.log', 'a') as new_map_log:
                        new_map_log.write(str(time.time()) + '\n')
                    sys.stdout.write('\nNew Map button clicked!\n')

            if now - last["captcha"] > t['captcha'] * 60:
                last["captcha"] = now
                robotCheck = captcha()
                if not robotCheck:
                     pyautogui.hotkey('ctrl', 'f5')
                     sys.stdout.write('\nRobot check fail.\n')
                     connected = False

            if now - last["refresh_heroes"] > t['refresh_heroes_positions'] * 60:
                last["refresh_heroes"] = now
                sys.stdout.write('\nRefreshing Heroes Positions.\n')
                refreshHeroesPositions()

            sys.stdout.flush()
            time.sleep(1)

        time.sleep(1)

        #clickBtn(teasureHunt)



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
