import time
from src.utils.number import addRandomness
from src.logger import logger, loggerMapClicked
import src.env as env
import src.bot.heroes as Heroes
import src.bot.login as Auth
import src.bot.action as Action
from src.bot.action import clickBtn
import sys

def run():
    time.sleep(5)
    t = env.cfg['time_intervals']

    last = {
        "login" : 0,
        "heroes" : 0,
        "new_map" : 0,
        "check_for_captcha" : 0,
        "refresh_heroes" : 0
    }

    while True:
        now = time.time()

        if now - last["heroes"] > addRandomness(t['send_heroes_for_work'] * 60):
            last["heroes"] = now
            Heroes.refreshHeroes()

        if now - last["login"] > addRandomness(t['check_for_login'] * 60):
            sys.stdout.flush()
            last["login"] = now
            Auth.login()

        if now - last["new_map"] > t['check_for_new_map_button']:
            last["new_map"] = now

            if clickBtn(env.images['new-map']):
                loggerMapClicked()

        if now - last["refresh_heroes"] > addRandomness( t['refresh_heroes_positions'] * 60):
            last["refresh_heroes"] = now
            Action.refreshHeroesPositions()

        logger(None, progress_indicator=True)

        sys.stdout.flush()

        time.sleep(1)