import pyautogui

import src.env as env
from src.logger import logger
from src.bot.action import clickBtn

def login():
    logger('😿 Checking if game has disconnected')

    if env.login_attempts > 3:
        logger('🔃 Too many login attempts, refreshing')
        env.login_attempts = 0
        pyautogui.hotkey('ctrl','f5')
        return

    if clickBtn(env.images['connect-wallet'], name='connectWalletBtn', timeout = 10):
        logger('🎉 Connect wallet button detected, logging in!')
        env.login_attempts = env.login_attempts + 1

    if clickBtn(env.images['select-wallet-2'], name='sign button', timeout=8):
        env.login_attempts = env.login_attempts + 1
        if clickBtn(env.images['treasure-hunt-icon'], name='teasureHunt', timeout = 15):
            env.login_attempts = 0
        return

    if not clickBtn(env.images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
        if clickBtn(env.images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', threshold  = env.threshold['select_wallet_buttons'] ):
            pass
    else:
        pass

    if clickBtn(env.images['select-wallet-2'], name='signBtn', timeout = 20):
        env.login_attempts = env.login_attempts + 1
        if clickBtn(env.images['treasure-hunt-icon'], name='teasureHunt', timeout=25):
            env.login_attempts = 0

    if clickBtn(env.images['ok'], name='okBtn', timeout=5):
        pass
