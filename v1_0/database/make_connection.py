from time import sleep
from dotenv import load_dotenv
from os import getenv
import mysql.connector
from mysql.connector import errorcode


def connect_database(attempt=3, delay=5):
    load_dotenv()
    database_config = {
        'host': getenv('DB_HOST'),
        'user': getenv('DB_USER'),
        'password': getenv('DB_PASS'),
        'database': getenv('DB_DTB'),
        'port': getenv('DB_PORT'),
    }

    for i in range(attempt):
        print('Connecting to database...')
        try:
            print('Connecting with success')
            conn = mysql.connector.connect(**database_config)
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('The database does not exit')
            else:
                print(f'Connection error: {err}')

            if i < attempt - 1:
                print(f'Retrying in {delay} seconds...')
                sleep(delay)

    print('Failed to connect to the database')
    return None
