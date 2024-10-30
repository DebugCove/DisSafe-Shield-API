import logging
from time import sleep
from os import getenv
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode


def load_database(retries=3, delay=5):
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()

    db_config = {
        'host': getenv('DB_HOST'),
        'user': getenv('DB_USER'),
        'password': getenv('DB_PASS'),
        'database': getenv('DB_DTB'),
        'port': getenv('DB_PORT'),
        #'ssl_ca': getenv('DB_SSL'),
    }

    if not isinstance(db_config, dict):
        logging.error('db_config must be a dictionary')
        exit()

    for i in range(retries):
        try:
            conn = mysql.connector.connect(**db_config)
            logging.info('Successful connection to the database')
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error('Something is wrong with the username or password.')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error('The database does not exist.')
            else:
                logging.error(f'Database error: {err}')
            if i < retries - 1:
                logging.error(f'Trying to reconnect in {delay} seconds...')
                sleep(delay)

    logging.error('Failed to connect to the database')
    return None
