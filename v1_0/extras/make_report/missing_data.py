def missing_data(data):
    required_fields = ['accuser_username', 'accuser_id', 'offender_username', 'offender_id', 'staff_username', 'staff_id', 'reason', 'server_id', 'bot', 'proof']


    if not isinstance(data, dict):
        return {
            'error': True,
            'message': 'Data is not a dictionary',
            'status_code': 500
        }

    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        return {
            'error': True,
            'message': f'Missing required fields: {" ".join(missing_fields)}',
            'status_code': 400
        }

    return {
        'error': False,
        'message': 'There no m,issing fields',
        'status_code': 200
    }
