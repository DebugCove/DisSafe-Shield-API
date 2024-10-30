import os
import time
import logging
import requests
import validators
from random import randint
import mysql.connector

def user_validation(id, username, status, timeout=5):
    logging.basicConfig(level=logging.DEBUG)
    if not isinstance(id, int):
        id = int(id)
    if not isinstance(username, str):
        username = str(username)

    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    if not TOKEN:
        logging.error('Token not found in .env file.')
        return {'status_code': 500, 'message': 'Internal Server Error'}
    url = f'https://discord.com/api/v10/users/{id}'
    headers = {'Authorization': f'Bot {TOKEN}'}

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        user_data = response.json()
        actual_username = user_data['username']
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.HTTPError):
            if e.response.status_code == 404:
                logging.error('User ID not found.')
                return {'status_code': 404, 'message': 'User ID not found.'}
            else:
                logging.error(f'Error in verification: {e}')
                return {
                    'status_code': e.response.status_code,
                    'message': 'Error in request.',
                }
        else:
            logging.error(f'Error in verification: {e}')
            return {'status_code': 500, 'message': 'Internal Server Error'}

    if actual_username == username and status == 'staff':
        logging.info('Staff username and ID match.')
        return {'status_code': 200, 'message': 'Staff username and ID match.'}
    elif actual_username == username and status == 'user':
        logging.info('User username and ID match.')
        return {'status_code': 200, 'message': 'User username and ID match.'}
    elif actual_username != username and status == 'staff':
        logging.error('Staff username and ID do not match.')
        return {'status_code': 400, 'message': 'Staff username and ID do not match.'}
    else:
        logging.error('User username and ID do not match.')
        return {'status_code': 400, 'message': 'User username and ID do not match.'}


def url_validation(proof, timeout=5):
    logging.basicConfig(level=logging.DEBUG)
    success = []
    success_but = []
    fails = []
    invalid = []

    if isinstance(proof, str):
        proof = proof.split(', ')

    for url in proof:
        if not validators.url(url):
            logging.error(f'Invalid URL: {url}')
            invalid.append(url)
            continue

        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                logging.info(f'URL {url} is valid.')
                success.append(url)
            else:
                logging.warning(f'URL {url} is not valid. Status code: {response.status_code}')
                success_but.append(url)
        except requests.exceptions.Timeout:
            logging.error(f'URL {url} cannot be reached -> Timeout')
            fails.append(f'URL {url} cannot be reached -> Timeout')
        except requests.exceptions.RequestException as e:
            logging.error(f'URL {url} cannot be reached -> ERROR: {e}')
            fails.append(f'The URL {url} cannot be reached -> ERROR: {e}')

    return {
        'success': success,
        'success_but': success_but,
        'fails': fails,
        'invalid': invalid,
    }


def unique_report_id_generator(retries=3, delay=5):
    logging.basicConfig(level=logging.DEBUG)
    db = load_database(retries, delay)
    if db:
        logging.info('Database connection successful.')
        try:
            cursor = db.cursor()
            query = 'SELECT id FROM Report'
            cursor.execute(query)
            ids = cursor.fetchall()
            new_id = randint(1111111111111111, 9999999999999999)
            logging.info(f'Generated new ID: {new_id}')
            while new_id in [row[0] for row in ids]:
                logging.warning(f'New ID {new_id} already exists. Generating new one...')
                new_id = randint(1111111111111111, 9999999999999999)
            logging.info(f'New ID generated: {new_id}')
            return new_id
        finally:
            logging.info('Closing database connection...')
            cursor.close()
            db.close()
    else:
        logging.error('Database connection failed.')
        db.close()
        return None


def token_validation(token, user_id, retries=3, delay=5):
    db = load_database(retries, delay)
    if db:
        try:
            cursor = db.cursor()
            query = 'SELECT COUNT(*) FROM Tokens WHERE token = %s AND user_id = %s'
            cursor.execute(query, (token, user_id))
            return bool(cursor.fetchone()[0])
        finally:
            cursor.close()
            db.close()
    else:
        db.close()
        return None


def check_duplicates(offender_id, server_id, retries=3, delay=5):
    db = load_database(retries, delay)
    if db:
        try:
            cursor = db.cursor()
            query = 'SELECT EXISTS (SELECT 1 FROM Report WHERE offender_id = %s AND server_id = %s)'
            cursor.execute(query, (offender_id, server_id))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            db.close()
    else:
        db.close()
        return None
