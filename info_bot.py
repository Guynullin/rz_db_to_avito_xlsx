import requests
import time
from config import BOT_TOKEN, CHAN_TOKEN, SSH_PASSWORD, DB_PASSWORD, CHAT_ID, CHAN_CHAT_ID

def send_message(message:str):
    flag = 0
    message = f"<<<RIMZONA to Avito Bot>>>\n{message}".replace(BOT_TOKEN, '<token>')\
        .replace(SSH_PASSWORD, '<pass>').replace(DB_PASSWORD, '<pass>')
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
            print(requests.get(url, timeout=60).json())
            break
        except requests.exceptions.ConnectionError as connecterr:
            print(connecterr)
            time.sleep(15)
            flag = 1
        except Exception as ex:
            print(ex)
            time.sleep(15)
        
