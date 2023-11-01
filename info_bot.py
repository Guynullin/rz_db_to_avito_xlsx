import requests
import time
import logging
from config import BOT_TOKEN, CHAN_TOKEN, SSH_PASSWORD, DB_PASSWORD, CHAT_ID, CHAN_CHAT_ID

def send_message(message:str):
    err = 0
    message = f"<<<RIMZONA to Avito Bot>>>\n{message}".replace(BOT_TOKEN, '<token>')\
        .replace(SSH_PASSWORD, '<pass>').replace(DB_PASSWORD, '<pass>')
    while True:
        try:
            if err >= 15:
                logging.error('Stopping the send_message function')
                break
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
            logging.info(requests.get(url, timeout=60).json())
            break
        except requests.exceptions.ConnectionError as connecterr:
            logging.error(connecterr)
            err += 1
            time.sleep(15)

        except Exception as ex:
            logging.error(ex)
            err += 1
            time.sleep(15)
        
