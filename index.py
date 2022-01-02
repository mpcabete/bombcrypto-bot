# -*- coding: utf-8 -*-    
from src.main import run
from src.main_multi_account import runMultiAccount
from src.utils.config import load_configs_from_file

config = load_configs_from_file()
run_multi_account = config['multiples_accounts_same_monitor']['enable']

if run_multi_account:
    runMultiAccount()
else:
    run()


