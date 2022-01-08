import time
import sys
import pygetwindow

from src.utils.number import addRandomness
import src.bot.logger as Log
import src.env as env
import src.bot.heroes as Heroes
import src.bot.login as Auth
import src.bot.action as Action

def runMultiAccount():
    time.sleep(5)
    intervals = env.cfg['time_intervals']

    windows = []
    title = env.multi_account_same_monitor['window_contains_title']

    Log.logger('🆗 Start')
    Log.logger('Searching for windows with contains title: {}'.format(title), color='yellow')

    for w in pygetwindow.getWindowsWithTitle(title):
        windows.append({
            "window": w,
            "login" : 0,
            "heroes" : 0,
            "new_map" : 0,
            "refresh_heroes" : 0
        })

    Log.logger('Found {} window(s):'.format(len(windows)), color='cyan')
    for index, last in enumerate(windows):
        Log.logger('{} -> {}'.format(index+1, last['window'].title), color='cyan')

    if len(windows) == 0:
        Log.logger('Exiting because dont have windows contains "{}" title'.format(title), color='red')
        exit()

    while True:
        now = time.time()
        
        for last in windows:
            env.window_object = last["window"]
            Log.logger('Client active window: {}'.format(last['window'].title), color='green')
            time.sleep(5)
            
            if now - last["login"] > addRandomness(intervals['check_for_login'] * 60):
                Action.activeWindow()
                sys.stdout.flush()
                last["login"] = now
                Auth.login()

            if now - last["heroes"] > addRandomness(intervals['send_heroes_for_work'] * 60):
                Action.activeWindow()
                last["heroes"] = now
                Heroes.refreshHeroes()

            if now - last["new_map"] > intervals['check_for_new_map_button']:
                Action.activeWindow()
                last["new_map"] = now
                Action.goToNextMap()

            if now - last["refresh_heroes"] > addRandomness( intervals['refresh_heroes_positions'] * 60):
                Action.activeWindow()
                last["refresh_heroes"] = now
                Action.refreshHeroesPositions()

            Log.logger(None, progress_indicator=True)
            sys.stdout.flush()

            time.sleep(1)
