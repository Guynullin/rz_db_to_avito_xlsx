import shutil
import psycopg2
import logging

from sshtunnel import SSHTunnelForwarder
from xlsx_api.record_xlsx import parse_xlsx
from info_bot import send_message
from collect_cards.get_cards_from_db import get_cards_from_db
from config import SSH_HOST, SSH_USERNAME, SSH_PASSWORD, LOCAL_HOST, LOCAL_PORT, REMOTE_PORT,\
DB_NAME, DB_USER, DB_PASSWORD, XLSX_PATH, LOGFILE


def main():
    logging.basicConfig(level=logging.INFO, filename=LOGFILE, filemode='a',\
                        format="%(asctime)s %(levelname)s %(message)s")

    try:
        with SSHTunnelForwarder(
            ssh_address_or_host = SSH_HOST,  
            ssh_username = SSH_USERNAME,
            ssh_password = SSH_PASSWORD,
            local_bind_address  = (LOCAL_HOST, LOCAL_PORT),
            remote_bind_address = (LOCAL_HOST, REMOTE_PORT)
        ) as server:
            logging.info('\n\n<main> Start')
            send_message('Start')
            server.start()

            params = {
                'database': DB_NAME,
                'user': DB_USER,
                'password': DB_PASSWORD,
                'host': LOCAL_HOST,
                'port': LOCAL_PORT
                }

            conn = psycopg2.connect(**params)
            cards_dict = get_cards_from_db(conn=conn)
            if cards_dict != 0:
                record = parse_xlsx(input_file_path=XLSX_PATH, db_cards=cards_dict)
                if record == 1:
                    send_message('Success')
                    logging.info('<main> Success')
        logging.info('<main> End\n\n')

    except Exception as ex:
        logging.error(f"{ex}\n\n")
        send_message(f"<<ERROR>>\n{ex}")
        


if __name__ == '__main__':
    main()

