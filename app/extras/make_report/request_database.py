import logging
import sys
import os
import mysql.connector
from mysql.connector import Error, InterfaceError, DatabaseError, IntegrityError, OperationalError


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.db import connect_database


def request_database(data):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nRequest database: make report\n\n')

    db = connect_database()
    if not db.is_connected():
        logging.error('Database connection was lost')
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }
    cursor = db.cursor()

    id = data.get('id')
    accuser_id = data.get('accuser_id')
    offender_id = data.get('offender_id')
    staff_id = data.get('staff_id')
    reason = data.get('reason')
    server_id = data.get('server_id')
    bot = data.get('bot')
    proof = data.get('proof')
    if isinstance(proof, str):
        proof = proof.split(', ')
    proof = [item.replace(']', '').replace('[', '') for item in proof]
    proof = str(proof)

    report_date = data.get('report_date')
    report_time = data.get('report_time')

    try:
        if cursor is None:
            logging.error('Failed to create database cursor')
            return {
                'error': True,
                'message': 'Internal Server Error',
                'status_code': 500
            }

        query = '''
            INSERT INTO Report 
            (id, accuser_id, offender_id, staff_id, reason, report_date, report_time, server_id, bot, proof) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (id, accuser_id, offender_id, staff_id, reason, report_date, report_time, server_id, bot, proof)
        cursor.execute(query, values)
        db.commit()
        logging.info('Report successfully inserted into the database')

        return {
            'error': False,
            'message': 'Report successfully created',
            'status_code': 201
        }

    except IntegrityError as integrity_error:
        logging.error('Integrity error: %s', integrity_error)
        return {
            'error': True,
            'message': 'Data integrity error',
            'status_code': 400
        }
    except OperationalError as operational_error:
        logging.error('Operational error: %s', operational_error)
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }
    except InterfaceError as interface_error:
        logging.error('Interface error: %s', interface_error)
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }
    except DatabaseError as database_error:
        logging.error('Database error: %s', database_error)
        return {
            'error': True,
            'message': 'General database error',
            'status_code': 500
        }
    except Error as mysql_error:
        logging.error('MySQL error: %s', mysql_error)
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }
    except Exception as error:
        logging.error('Unexpected error: %s', error)
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
