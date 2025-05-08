import uuid
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from extras.info_generator import generate_date, generate_time
from database.make_connection import connect_database



def generator_uuid_id():
    new_id = str(uuid.uuid4()).replace('-', '')
    return new_id[:10]

def id_generator():
    query = 'SELECT id FROM Logs WHERE %s'
    conn = connect_database()
    if conn is None:
        return {
            'error': True,
            'message': 'Error when trying to connect to the database', 
            'status_code': 500
        }

    id = generator_uuid_id()
    cursor = conn.cursor()
    cursor.execute(query, (id,))
    result = cursor.fetchone()

    while result != None:
        id = generator_uuid_id()
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()

    return {
        'error': False,
        'message': 'ID was created successfully',
        'status_code': 200,
        'data': {
            'id': id
        }
    }


def logs_for_database(type, message):
    if type is None:
        return {
            'error': True,
            'message': 'Type is null',
            'status_code': 500
        }
    if type not in ['error','debug', 'info', 'warning', 'critical']:
        return  {
            'error': True,
            'message': 'Type in logs is not valid',
            'status_code': 500
        }

    if message is None:
        return {
            'error': True,
            'message': 'Message is null',
            'status_code': 500
        }

    result = id_generator()
    if result['error']:
        return result
    
    id = result['data']['id']