import logging
import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.db import connect_database


def report_id_generator():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nGenerate ID  report')
    db = connect_database()
    logging.info('Trying to acess the databse')
    if not db:
        logging.error('Error trying to acess the databse')
        return {
            'error': True,
            'message': 'Error trying to acess the database.',
            'status_code': 500
        }

    try:
        if not db.is_connected():
            logging.error('Error trying to acess the databse')
            return {
                'error': True,
                'message': 'Error trying to acess the database.',
                'status_code': 500
            }

        cursor = db.cursor()
        query = 'SELECT id FROM Report'

        if not cursor:
            logging.error('Error getting the cursor')
            return {
                'error': True,
                'message': 'Error getting the cursor.',
                'status_code': 500
            }

        cursor.execute(query)
        logging.info('Execute the query in the database')
        ids = cursor.fetchall()

        new_id = str(uuid.uuid4()).replace('-', '')
        formated_new_id = new_id[:10]
        while formated_new_id in [row[0] for row in ids]:
            logging.warning('ID: %s already exists. Generating new one...', formated_new_id)
            new_id = str(uuid.uuid4()).replace('-', '')
            formated_new_id = new_id[:10]

        logging.info('Generated new ID: %s', formated_new_id)

        return {
            'error': False,
            'message': 'New ID generated',
            'status_code': 201,
            'data': formated_new_id
        }
    except Exception as e:
        logging.error('Unexpected error: %s', e)
        return {
            'error': True,
            'message': 'Unexpected error',
            'status_code': 500
        }
