from cv2 import cv2
import numpy as np
import mss
import pyautogui
import time
import datetime
import sys

import yaml

from gain_calculator import *



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
green_bar = cv2.imread('targets/green-bar.png')
chest_img = cv2.imread('targets/chest.png')


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

    commoms = positions(commom_img, trashhold = ct['commom'])
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
    buttons = positions(go_work_img, trashhold=ct['go_to_work_btn'])
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
    green_bars = positions(green_bar, trashhold=ct['green_bar'])
    buttons = positions(go_work_img, trashhold=ct['go_to_work_btn'])

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
        sys.stdout.write('\ntoo many login attempts, refreshing.')
        login_attempts = 0
        pyautogui.press('f5')
        return

    if clickBtn(connect_wallet_btn_img, name='connectWalletBtn', timeout = 10):
        sys.stdout.write('\nConnect wallet button detected, logging in!')
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
        if clickBtn(select_wallet_hover_img, name='selectMetamaskHoverBtn', trashhold = ct['select_wallet_buttons'] ):
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

def calculate_BCOIN(chest_img):
    
    clickBtn(chest_img)

    time.sleep(3)

    screen = printSreen()

    screen = preprocess_image(screen)

    location_list_screen = find_digits_locations(screen)
    
    location_list_screen = filter_digits(location_list_screen)

    digit_crops_screen = get_crops(screen, location_list_screen)
    
    bcoin = compute_results(digit_crops_screen)

    print(f'Actual BCOIN = {bcoin}')

    goToGame()
    
    return bcoin


def main():
    time.sleep(5)
    t = c['time_intervals']

    last = {
    "login" : 0,
    "heroes" : 0,
    "new_map" : 0,
    "refresh_heroes" : 0,
    "snap_coin": 0
    }

    bcoin_track = {
        "last_value": 0,
        "num_shap_coin": 0,
        "tot_gain": 0
    }

    starting_datetime = datetime.datetime.now()

    print(f'\nStarting at {starting_datetime.strftime("%H:%M day %d/%m/%Y")}')

    while True:
        now = time.time()

        if bcoin_track['last_value'] == 0:
            try:
                last['snap_coin'] = now
                sys.stdout.write('\nCheck current BCOIN.')
                bcoin = calculate_BCOIN(chest_img)
                sys.stdout.write(f'\nYou start from {bcoin} BCOIN')
                bcoin_track['last_value'] = bcoin
                with open('bcoin_gain.log','a') as bcoin_log:
                    bcoin_log.write(f'{datetime.datetime.now()},0')
                #bcoin_track['num_shap_coin'] += 1
                sys.stdout.write("\n")
            except Exception as e:                
                sys.stdout.write('\nSomething wrong with BCOIN computation')
                print(e)
                sys.stdout.write("\n")

        if now - last['snap_coin'] >= 60*60: # 1 hour
            try:
                last['snap_coin'] = now
                sys.stdout.write('\nCheck current BCOIN.')
                bcoin = calculate_BCOIN(chest_img)
                bcoin_track['tot_gain'] += (bcoin - bcoin_track['last_value'])
                bcoin_track['last_value'] = bcoin
                bcoin_track['num_shap_coin'] += 1
                hour_mean = bcoin_track['tot_gain'] / bcoin_track['num_shap_coin']

                with open('bcoin_gain.log','a') as bcoin_log:
                    bcoin_log.write(f'{datetime.datetime.now()},{bcoin_track["tot_gain"]}')

                sys.stdout.write(f"\nYou made {bcoin_track['tot_gain']} BCOIN")
                sys.stdout.write(f"\nYou made {hour_mean} BCOIN/hour")
                sys.stdout.write("\n")
            except:
                sys.stdout.write('\nSomething wrong with BCOIN computation')
                sys.stdout.write("\n")

        
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
            if clickBtn(new_map_btn_img):
                with open('new-map.log','a') as new_map_log:
                    new_map_log.write(str(datetime.datetime.now())+'\n')
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
