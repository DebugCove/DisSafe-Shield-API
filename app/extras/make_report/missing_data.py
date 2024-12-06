def missing_data(data):
    required_fields = ['accuser_username', 'accuser_id', 'offender_username', 'offender_id', 'staff_username', 'staff_id', 'reason', 'server_id', 'bot', 'proof']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {
            'error': True,
            'message': f'Missing required fields:{" ".join(missing_fields)}',
            'status_code': 400
        }
    return {
        'error': False,
        'message': 'There are no missing fields',
        'status_code': 200
    }
