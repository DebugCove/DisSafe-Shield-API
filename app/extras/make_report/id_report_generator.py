import logging
import sys
import os
import uuid
import mysql

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.db import connect_database


def report_id_generator():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nGenerate ID report')

    db = connect_database()
    logging.info('Trying to access the database')
    if not db:
        logging.error('Error trying to access the database')
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
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

        query = 'SELECT id FROM Report'
        cursor.execute(query)
        logging.info('Executed the query in the database')
        ids = cursor.fetchall()

        new_id = str(uuid.uuid4()).replace('-', '')
        formatted_new_id = new_id[:10]
        while formatted_new_id in [row[0] for row in ids]:
            logging.warning('ID: %s already exists. Generating new one...', formatted_new_id)
            new_id = str(uuid.uuid4()).replace('-', '')
            formatted_new_id = new_id[:10]

        logging.info('Generated new ID: %s', formatted_new_id)

        return {
            'error': False,
            'message': 'New ID generated',
            'status_code': 201,
            'data': formatted_new_id
        }
    except mysql.connector.Error as err:
        logging.error('Database error: %s', err)
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
        if db and db.is_connected():
            db.close()
            logging.info('Database connection closed')
