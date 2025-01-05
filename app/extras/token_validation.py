import logging
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.db import connect_database


def token_validation(auth_header):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nToken Validation\n')

    load_dotenv()
    db = connect_database()
    if db is None:
        logging.error('Error trying to acess the databse')
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }

    if auth_header and auth_header.startswith('Bearer '):
        try:
            token = auth_header.split()[1]
            if token is None:
                logging.error('The token entered is not valid format')
                return {
                    'error': True,
                    'message': 'Not valid token format',
                    'status_code': 400
                }
            cursor = db.cursor()
            query = 'SELECT * FROM Tokens WHERE token = %s'
            cursor.execute(query, (token,))
            logging.info('Execute the query in the database')
            result = cursor.fetchone()
            if result is None:
                logging.error('The token entered was not found in the database')
                return {
                    'error': True,
                    'message': 'Token is invalid',
                    'status_code': 401
                }
            else:
                logging.info('The token entered was found in the databse')
                return {
                    'error': False,
                    'message': 'Token is valid',
                    'status_code': 201
                }

        except IndexError:
            logging.error('The token entered is not valid format')
            return {
                'error': True,
                'message': 'Not valid token format',
                'status_code': 400
            }
    else:
        logging.error('The token is not provided or invalid')
        return {
            'error': True,
            'message': 'Token not provided or invalid',
            'status_code': 401
        }
