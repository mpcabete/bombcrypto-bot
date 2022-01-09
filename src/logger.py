from src.date import dateFormatted

import sys
import yaml
import requests

stream = open("./config.yaml", 'r')
c = yaml.safe_load(stream)

last_log_is_progress = False

COLOR = {
    'blue': '\033[94m',
    'default': '\033[99m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}

def telegram_bot_sendtext(bot_message):
    if c['telegram']['token_api'] != 'disable' and c['telegram']['chat_id'] != 'disable' and type(bot_message) == str:
        bot_token = c['telegram']['token_api']
        bot_chatID = c['telegram']['chat_id']
        send_text = 'https://api.telegram.org/bot' + str(bot_token) + '/sendMessage?chat_id=' + str(bot_chatID) + '&parse_mode=Markdown&text=' + str(bot_message)
        response = requests.get(send_text)
        return response.json()

def logger(message, progress_indicator = False, color = 'default'):
    telegram_bot_sendtext(message)
    global last_log_is_progress
    color_formatted = COLOR.get(color.lower(), COLOR['default'])

    formatted_datetime = dateFormatted()
    formatted_message = "[{}] => {}".format(formatted_datetime, message)
    formatted_message_colored  = color_formatted + formatted_message + '\033[0m'

    
    # Start progress indicator and append dots to in subsequent progress calls
    if progress_indicator:
        if not last_log_is_progress:
            last_log_is_progress = True
            formatted_message = color_formatted + "[{}] => {}".format(formatted_datetime, '⬆️ Processing last action..')
            sys.stdout.write(formatted_message)
        else:
            sys.stdout.write(color_formatted + '.')
        sys.stdout.flush()
        return

    if last_log_is_progress:
        sys.stdout.write('\n')
        sys.stdout.flush()
        last_log_is_progress = False    

    print(formatted_message_colored)

    if (c['save_log_to_file'] == True):
        with open("./logs/logger.log", "a", encoding='utf-8') as logger_file:
            logger_file.write(formatted_message + '\n')
            logger_file.close()

    return True

def loggerMapClicked():
    logger('🗺️ New Map button clicked!')
    with open("./logs/new-map.log", "a", encoding='utf-8') as logger_file:
        logger_file.write(dateFormatted() + '\n')
        logger_file.close()
