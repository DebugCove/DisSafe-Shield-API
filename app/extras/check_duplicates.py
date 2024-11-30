import logging
import sys
import os
import mysql.connector
from mysql.connector import errorcode

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.db import connect_database


def check_duplicates(data):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nCheck duplicates report')

    if not data:
        logging.error('No data was provided')
        return {
            'error': True,
            'message': 'No data was provided.',
            'status_code': 400
        }

    db = connect_database()
    logging.info('Trying to access the database')
    if not db:
        logging.error('Error trying to access the database')
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }

    offender_id = data.get('offender_id')
    server_id = data.get('server_id')

    if not offender_id or not server_id:
        logging.error('offender_id or server_id were not provided')
        return {
            'error': True,
            'message': 'offender id or server id were not provided.',
            'status_code': 400
        }

    try:
        if not db.is_connected():
            logging.error('Database connection was lost')
            return {
                'error': True,
                'message': 'Internal Server Error',
                'status_code': 500
            }

        cursor = db.cursor()
        if cursor is None:
            logging.error('Failed to create database cursor')
            return {
                'error': True,
                'message': 'Internal Server Error',
                'status_code': 500
            }

        query = 'SELECT EXISTS (SELECT 1 FROM Report WHERE offender_id = %s AND server_id = %s)'
        cursor.execute(query, (offender_id, server_id))
        result = cursor.fetchone()

        if result and result[0]:
            return {
                'error': True,
                'message': 'Report is duplicate',
                'status_code': 400
            }
        return {
            'error': False,
            'message': 'Report is not duplicate',
            'status_code': 200
        }

    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error('Something is wrong with your user name or password')
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error('The database does not exist')
        else:
            logging.error(f'Connection error: {e}')

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
        if db.is_connected():
            cursor.close()
            db.close()
