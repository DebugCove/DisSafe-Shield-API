import logging


def missing_data(data):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nChecking missing data\n')

    required_fields = ['accuser_username', 'accuser_id', 'offender_username', 'offender_id', 'staff_username', 'staff_id', 'reason', 'server_id', 'bot', 'proof']

    if not isinstance(data, dict):
        logging.error('Data is not a dictionary')
        return {
            'error': True,
            'message': 'Data is not a dictionary',
            'status_code': 400
        }

    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        logging.error('Some fields are missing')
        return {
            'error': True,
            'message': f'Missing required fields:{" ".join(missing_fields)}',
            'status_code': 400
        }
    logging.info('No missing fields')
    return {
        'error': False,
        'message': 'There are no missing fields',
        'status_code': 200
    }
