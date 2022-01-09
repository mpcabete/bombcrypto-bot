
import sys
import yaml
import requests

# Load config file.
stream = open("config.yaml", 'r')
c = yaml.safe_load(stream)

def telegram_bot_sendtext(bot_message):
    if c['telegram']['level'] != 'disable' and type(bot_message) == str:
        bot_token = c['telegram']['token_api']
        bot_chatID = c['telegram']['chat_id']
        if bot_token != 'your_bot_token' and bot_chatID != 'yout_chat_id':
            telegram_payload = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
            response = requests.get(telegram_payload)
            return response.json()