import logging
from time import sleep
from os import getenv
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode


def connect_database(retries=3, delay=5):
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()

    database_config = {
        'host': getenv('DB_HOST'),
        'user': getenv('DB_USER'),
        'password': getenv('DB_PASS'),
        'database': getenv('DB_DTB'),
        'port': getenv('DB_PORT'),
    }

    if getenv('FLASK_ENV') == 'development':
        database_config['database'] = getenv('DB_DTB_TESTING')

    for i in range(retries):
        logging.info('Connecting to database...')
        try:
            conn = mysql.connector.connect(**database_config)
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error('The database does not exit')
            else:
                logging.error(f'Connection error: {err}')

            if i < retries - 1:
                logging.info(f'Retrying in {delay} seconds...')
                sleep(delay)

    logging.error('Failed to connect to the database')
    return None
