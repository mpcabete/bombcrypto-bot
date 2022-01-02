# -*- coding: utf-8 -*-    
from src.main import run
from src.main_multi_account import runMultiAccount
from src.utils.config import load_configs_from_file
from src.bot.logger import logger

config = load_configs_from_file()
run_multi_account = config['multiples_accounts_same_monitor']['enable']

logger('Bombcrypto BOT starting', color='yellow')

if run_multi_account:
    logger('Running bot for MULTI ACCOUNT ON SAME MONITOR', color='cyan')
    runMultiAccount()
else:
    logger('Running bot', color='cyan')
    run()
