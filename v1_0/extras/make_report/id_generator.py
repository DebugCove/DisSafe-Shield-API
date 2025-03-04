import uuid
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from database.make_connection import connect_database



def generator_uuid_id():
    new_id = str(uuid.uuid4()).replace('-', '')
    return new_id[:10]

def id_generator():
    query = 'SELECT id FROM Report WHERE %s'
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
        'message': 'Id foi criado com sucesso',
        'status_code': 200,
        'data': {
            'id': id
        }
    }
