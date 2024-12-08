import requests
import logging
from dotenv import load_dotenv
from os import getenv


def user_validation(data, status):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nUser validation\n')

    load_dotenv()
    if not data or not status:
        logging.error('Data or status is not defined')
        return {
            'error': True,
            'message': 'Data or status is not defined',
            'status_code': 400
        }

    if status == "staff":
        logging.info('Checking the staff member')
        id = data.get('staff_id')
        username = data.get('staff_username')
    else:
        logging.info('Checking the member')
        id = data.get('accuser_id')
        username = data.get('accuser_username')

    if not id or not username:
        logging.error('ID or username is not defined')
        return {
            'error': True,
            'message': 'Id or username not found',
            'status_code': 400
        }

    TOKEN = getenv('TOKEN')
    if not TOKEN:
        logging.error('Token is not defined')
        return {
            'error': True,
            'message': 'Internal Server Error',
            'status_code': 500
        }

    url = f'https://discord.com/api/v10/users/{id}'
    headers = {'Authorization': f'Bot {TOKEN}'}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        logging.info('Requesting the discord API')
        response.raise_for_status()
        user_data = response.json()
        current_user = user_data.get('username')
        logging.info('Receiving data from the API')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logging.error('User not found')
            return {
                'error': True,
                'message': 'User not found',
                'status_code': 404
            }
        else:
            logging.error('Error in request %s', e)
            return {
                'error': True,
                'message': 'Error',
                'status_code': e.response.status_code
            }
    except requests.exceptions.RequestException as e:
        logging.error('Error in request %s', e)
        return {
            'error': True,
            'message': 'Error in request',
            'status_code': 400
        }

    if current_user == username and status == 'staff':
        logging.info('Staff username: %s and ID match %s', current_user, id)
        return {
            'error': False,
            'message': 'Staff username and ID match',
            'status_code': 200
        }
    elif current_user == username and status == 'user':
        logging.info('User username: %s and ID match %s', current_user, id)
        return {
            'error': False,
            'message': 'User username and ID match',
            'status_code': 200
        }
    elif current_user != username and status == 'staff':
        logging.info('Staff username: %s and ID not match %s', current_user, id)
        return {
            'error': True,
            'message': 'Staff username not match with id ',
            'status_code': 400
        }
    elif current_user != username and status == 'user':
        logging.info('User username: %s and ID not match %s', current_user, id)
        return {
            'error': True,
            'message': 'User username not match with id',
            'status_code': 400
        }
