import logging
import sys
import os
import mysql.connector
from mysql.connector import errorcode

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.db import connect_database

def get_all_report():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nGet all info report\n')

    information_list = [
        'id',
        'accuser_id',
        'offender_id',
        'staff_id',
        'reason',
        'date',
        'time',
        'server_id',
        'bot',
        'proof'
    ]

    db = connect_database()
    logging.info('Attempting to connect to the database')
    if db is None or not db.is_connected():
        logging.error('Failed to connect to the database')
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }

    cursor = None
    try:
        cursor = db.cursor()
        query = 'SELECT * FROM Report'
        cursor.execute(query)
        logging.info('Query executed successfully')
        result = cursor.fetchall()

        if result:
            logging.info('Reports found')
            result_formatted = [
                {name: value for name, value in zip(information_list, row)}
                for row in result
            ]

            return {
                'error': False,
                'message': 'Reports successfully found',
                'status_code': 200,
                'data': result_formatted
            }
        else:
            logging.info('No reports found')
            return {
                'error': True,
                'message': 'No reports found',
                'status_code': 404
            }

    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error('Access denied: Invalid username or password')
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error('Database does not exist')
        else:
            logging.error(f'Database connection error: {e}')
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }

    except Exception as e:
        logging.error('Unexpected error: %s', e)
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }

    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()
            logging.info('Database connection closed')
