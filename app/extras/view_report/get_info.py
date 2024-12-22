import logging
import sys
import os
import mysql.connector
from mysql.connector import errorcode

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.db import connect_database

def get_info_report(report_id):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nGet unique info report\n')

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

    if not report_id:
        logging.error('No report ID was provided')
        return {
            'error': True,
            'message': 'No report ID was provided.',
            'status_code': 400
        }

    db = connect_database()
    logging.info('Attempting to connect to the database')
    if not db or not db.is_connected():
        logging.error('Failed to connect to the database')
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }

    cursor = None
    try:
        cursor = db.cursor()
        query = 'SELECT * FROM Report WHERE id = %s'
        cursor.execute(query, (report_id,))
        logging.info('Query executed successfully')
        result = cursor.fetchone()

        if result:
            logging.info('Report found in the database')
            result_formatted = {name: info for name, info in zip(information_list, result)}

            return {
                'error': False,
                'message': 'Report successfully found',
                'status_code': 200,
                'data': result_formatted
            }

        else:
            logging.warning('Report not found')
            return {
                'error': True,
                'message': 'Report not found',
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
        if db.is_connected():
            db.close()
