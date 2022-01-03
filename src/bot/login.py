from time import sleep
import pyautogui

import src.env as env
import src.bot.logger as Log
from src.bot.action import clickBtn, closeMetamaskWindow, getPositions
from src.decorators.check_metamask_notification import checkMetamaskNotification

def login():
    Log.logger('😿 Checking if game has disconnected')
    sleep(5)

    # if env.login_attempts > 3:
    #     Log.logger('🔃 Too many login attempts, refreshing')
    #     env.login_attempts = 0
    #     pyautogui.hotkey('ctrl','f5')
    #     return

    already_refreshed = False
    if clickBtn(env.images['ok'], name='okBtn', timeout=5):
        already_refreshed = True
    sleep(15)

    closeMetamaskWindow()
    if not already_refreshed:
        in_login_screen = getPositions(env.images['connect-wallet'], threshold=env.threshold['default'])
        if(len(in_login_screen)!=0):
            pyautogui.hotkey('ctrl','f5')

    Log.logger('Loggin attempt: {}'.format(env.login_attempts), color='yellow')
    in_login_screen = getPositions(env.images['connect-wallet'], threshold=env.threshold['default'])
    if(len(in_login_screen)==0):
        Log.logger('Already logged...', color='cyan')
        return
    else:
        Log.logger('Logging process start...', color='cyan')

    sleep(10)

    if clickBtn(env.images['connect-wallet'], name='connectWalletBtn', timeout = 10):
        Log.logger('🎉 Connect wallet button detected, logging in!')
        env.login_attempts = env.login_attempts + 1

    if clickOnSignIn():
        env.login_attempts = env.login_attempts + 1
        if clickBtn(env.images['treasure-hunt-icon'], name='teasureHunt', timeout = 15):
            env.login_attempts = 0
        return

    if clickBtn(env.images['ok'], name='okBtn', timeout=5):
        pass

@checkMetamaskNotification
def clickOnSignIn():
    env.in_login_process = True
    env.force_full_screen = True
    result = clickBtn(env.images['select-wallet-2'], name='sign button', timeout=8)
    env.in_login_process = False
    env.force_full_screen = False
    return result