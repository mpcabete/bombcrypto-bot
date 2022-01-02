import time
from src.utils.number import addRandomness
import src.logger as log
import src.env as env
import src.bot.heroes as Heroes
import src.bot.login as Auth
import src.bot.action as Action
from src.bot.action import clickBtn
import sys
import pygetwindow

def runMultiAccount():
    time.sleep(5)
    t = env.cfg['time_intervals']

    windows = []
    log.logger('🆗 Start using MULTIPLES ACCOUNTS TO ONE MONITOR SUPPORT')

    for w in pygetwindow.getWindowsWithTitle('bombcrypto'):
        windows.append({
            "window": w,
            "login" : 0,
            "heroes" : 0,
            "new_map" : 0,
            "check_for_captcha" : 0,
            "refresh_heroes" : 0
        })

    while True:
        now = time.time()
        
        for last in windows:
            env.window_object = last["window"]

            log.logger('Client activated window!\n---> {}'.format(last['window'].title))
            time.sleep(5)

            if now - last["heroes"] > addRandomness(t['send_heroes_for_work'] * 60):
                Action.active_window()
                last["heroes"] = now
                Heroes.refreshHeroes()

            if now - last["login"] > addRandomness(t['check_for_login'] * 60):
                Action.active_window()
                sys.stdout.flush()
                last["login"] = now
                Auth.login()

            if now - last["new_map"] > t['check_for_new_map_button']:
                Action.active_window()
                last["new_map"] = now

                if clickBtn(env.images['new-map']):
                    log.loggerMapClicked()

            if now - last["refresh_heroes"] > addRandomness( t['refresh_heroes_positions'] * 60):
                Action.active_window()
                last["refresh_heroes"] = now
                Action.refreshHeroesPositions()

            log.logger(None, progress_indicator=True)
            sys.stdout.flush()

            time.sleep(1)
