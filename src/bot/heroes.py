import time
import pyautogui

import src.env as env
import src.bot.logger as Log
from src.bot.action import goToGame, goToHeroes, moveToWithRandomness, scroll, getPositions
from src.bot.utils import isHome, isWorking

def clickButtons():
    buttons = getPositions(env.images['go-work'], threshold=env.threshold['go_to_work_btn']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['go_to_work_btn'])
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x+(w/2),y+(h/2),1)
        pyautogui.click()
        env.hero_clicks = env.hero_clicks + 1
        if env.hero_clicks > 20:
            Log.logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(buttons)

def clickGreenBarButtons():
    offset = 130

    green_bars = getPositions(env.images['green-bar'], threshold=env.threshold['green_bar']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['green_bar'])
    Log.logger('🟩 %d green bars detected' % len(green_bars))
    buttons = getPositions(env.images['go-work'], threshold=env.threshold['go_to_work_btn']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['go_to_work_btn'])
    Log.logger('🆗 %d buttons detected' % len(buttons))


    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        Log.logger('🆗 %d buttons with green bar detected' % len(not_working_green_bars))
        Log.logger('👆 Clicking in %d heroes' % len(not_working_green_bars))

    for (x, y, w, h) in not_working_green_bars:
        pos_click_x = x+offset+(w/2)
        pos_click_y = y+(h/2)
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        env.hero_clicks = env.hero_clicks + 1
        if env.hero_clicks > 20:
            Log.logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(not_working_green_bars)

def clickFullBarButtons():
    offset = 100
    full_bars = getPositions(env.images['full-stamina'], threshold=env.threshold['default']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['default'])
    buttons = getPositions(env.images['go-work'], threshold=env.threshold['go_to_work_btn']*env.scale_image['threshold'] if env.scale_image['enable'] else env.threshold['go_to_work_btn'])

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        Log.logger('👆 Clicking in %d heroes' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        
        pos_click_x = x+offset+(w/2)
        pos_click_y = y+(h/2)
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        env.hero_clicks = env.hero_clicks + 1

    return len(not_working_full_bars)

def sendHeroesHome():
    if not env.home['enable']:
        return
    heroes_positions = []
    for hero in env.home_heroes:
        hero_positions = getPositions(hero, threshold=env.home['hero_threshold'])
        if not len (hero_positions) == 0:
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)

    go_home_buttons = getPositions(env.images['send-home'], threshold=env.home['home_button_threshold'])
    go_work_buttons = getPositions(env.images['go-work-old'], threshold=env.threshold['go_to_work_btn'])

    for position in heroes_positions:
        if not isHome(position,go_home_buttons):
            if(not isWorking(position, go_work_buttons)):
                print ('hero not working, sending him home')
                
                pos_click_x = go_home_buttons[0][0]+go_home_buttons[0][2]/2
                pos_click_y = position[1]+position[3]/2
                moveToWithRandomness(pos_click_x,pos_click_y,1)
                pyautogui.click()
            else:
                print ('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')

def refreshHeroes():
    Log.logger('🏢 Search for heroes to work')

    goToHeroes()

    if env.cfg['select_heroes_mode'] == "full":
        Log.logger('⚒️ Sending heroes with full stamina bar to work', 'green')
    elif env.cfg['select_heroes_mode'] == "green":
        Log.logger('⚒️ Sending heroes with green stamina bar to work', 'green')
    else:
        Log.logger('⚒️ Sending all heroes to work', 'green')

    buttonsClicked = 1
    empty_scrolls_attempts = env.cfg['scroll_attemps']

    while(empty_scrolls_attempts >0):
        if env.cfg['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons()
        elif env.cfg['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked = clickButtons()

        sendHeroesHome()

        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        time.sleep(2)
    Log.logger('💪 {} heroes sent to work'.format(env.hero_clicks))
    goToGame()
