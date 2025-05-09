import sys
import os
from mysql.connector import Error, InterfaceError, DatabaseError, IntegrityError, OperationalError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from database.make_connection import connect_database


def send_database(data):
    QUERY = '''
        INSERT INTO Report
        (id, accuser_id, offender_id, staff_id, reason, report_date, report_time, server_id, bot, proof, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    conn = connect_database()
    if conn is None:
        print('Error when trying to connect to the database')
        return {
            'error': True,
            'message': 'Error when trying to connect to the database', 
            'status_code': 500
        }

    cursor = conn.cursor()
    if cursor is None:
        print('Fail to connect to database')
        return {
            'error': True,
            'message': 'Fail to connect to database',
            'status_code': 500
        }

    id = data.get('id')
    accuser_id = data.get('accuser_id')
    offender_id = data.get('offender_id')
    staff_id = data.get('staff_id')
    reason = data.get('reason')
    server_id = data.get('server_id')
    bot = data.get('bot')
    proof = data.get('proof')
    date = data.get('date')
    time = data.get('time')
    status = 'open'

    try:
        values = (id, accuser_id, offender_id, staff_id, reason, date, time, server_id, bot, proof, status)
        cursor.execute(QUERY, values)
        conn.commit()
        return {
            'error': False,
            'message': 'Report successufly created',
            'status_code': 200
        }
    except IntegrityError as error:
        print(f'Integrity error: {error}')
        return {
            'error': True,
            'message': f'Integrity error: {error}',
            'status_code': 500
        }
    except OperationalError as error:
        print(f'Operational error: {error}')
        return {
            'error': True,
            'message': f'Operational error: {error}',
            'status_code': 500
        }
    except InterfaceError as error:
        print(f'Interface error: {error}')
        return {
            'error': True,
            'messasge': f'Interface error: {error}',
            'status_code': 500
        }
    except DatabaseError as error:
        print(f'Database error: {error}')
        return {
            'error': True,
            'message': f'Database error: {error}',
            'status_code': 500
        }
    except Error as error:
        print(f'Error mysql: {error}')
        return {
            'error': True,
            'message': f'Error mysql: {error}',
            'status_code': 500
        }
    except Exception as error:
        print(f'Error  exception mysql: {error}')
        return {
            'error': True,
            'message': f'Error mysql: {error}',
            'status_code': 500
        }
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
