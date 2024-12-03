import logging
from time import sleep
from os import getenv
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

#def generate_connection(retries=3, delay=5):  //Code recommendation
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


"""
from flask import g
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
def connect_database():
    if not g.get('db'):
        logging.error("Dont have connection")
        g.db = generate_connection()
    return g.db if isinstance(g.db, PooledMySQLConnection | MySQLConnectionAbstract) else None

It's a code recommendation. I believe this change will maybe enable the database in tests. 
Moreover, the use of the g object from Flask for the database is shown in examples 
in the Flask documentation.
"""