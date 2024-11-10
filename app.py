import logging
import mysql.connector
from os import urandom 
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, abort
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

from extras.config import user_validation, url_validation, unique_report_id_generator, token_validation, check_duplicates
from config.database import load_database
from config.run_project import run_project
from middleware.compression import compression


app = Flask(__name__)
compression(app)
CORS(app)
app.secret_key = urandom(24)

Talisman(
    app,
    frame_options='DENY',
    x_xss_protection=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=['500 per day'],
    storage_uri='redis://localhost:6379'
)


@app.route('/', methods=['GET'])
@app.route('/api/v1', methods=['GET'])
def api():
    params = request.args
    if params:
        return jsonify({'message': 'This route does not accept parameters'}), 400
    else:
        return jsonify({'message': 'DisSafe Shield API'}), 200

@app.route('/api/v1/report', methods=['POST'])
@limiter.limit('5 per minute')
def report():
    params = request.args
    if params:
        return jsonify({'message': 'This route does not accept parameters'}), 400

    data = request.get_json()

    required_fields = ['accuser_username', 'accuser_id', 'offender_username', 'offender_id', 'staff_username', 'staff_id', 'reason', 'server_id', 'bot', 'proof']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return abort(400, description=f'Missing required fields: {", ".join(missing_fields)}')

    staff_username = data.get('staff_username')
    staff_id = data.get('staff_id')
    validation = user_validation(staff_id, staff_username, status='staff')
    if validation['status_code'] not in range(200, 299):
        return jsonify({'message': validation['message']}), validation['status_code']

    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        try:
            token = auth_header.split(' ')[1]
            if not token_validation(token, staff_id):
                return jsonify({'message': 'Token not provided or valid'}), 401
        except IndexError:
            return jsonify({'message': 'Invalid token format'}), 400
    else:
        return jsonify({'message': 'Token not provided or invalid'}), 401

    report_id = unique_report_id_generator()
    while report_id is None:
        report_id = unique_report_id_generator()

    accuser_username = data.get('accuser_username')
    accuser_id = int(data.get('accuser_id'))
    validation = user_validation(accuser_id, accuser_username, status='user')
    if validation['status_code'] != 200:
        return jsonify({'message': validation['message']}), validation['status_code']

    offender_username = data.get('offender_username')
    offender_id = int(data.get('offender_id'))
    validation = user_validation(offender_id, offender_username, status='user')
    if validation['status_code'] != 200:
        return jsonify({'message': validation['message']}), validation['status_code']

    reason = data.get('reason')
    if not isinstance(reason, str):
        return jsonify({'message': 'Reason not valid'}), 400

    current_date = datetime.now()
    report_date = current_date.strftime('%Y-%m-%d')
    report_time = current_date.strftime('%H:%M:%S')

    server_id = data.get('server_id')
    if not isinstance(server_id, int):
        return jsonify({'message': 'Server ID must be an integer'}), 400

    if check_duplicates(offender_id, server_id):
        return jsonify({'message': 'You have already reported this user'}), 400

    bot = data.get('bot')
    if not isinstance(bot, bool) or not isinstance(bot, int):
        return jsonify({'message': 'Bot not valid'}), 400

    proof = data.get('proof')
    if not isinstance(proof, list) and not isinstance(proof, str):
        return jsonify({'message': 'Proof not valid'}), 400
    url_valid = url_validation(proof)
    url_success = url_valid['success']
    url_success_but = url_valid['success_but']
    url_fails = url_valid['fails']
    url_invalid = url_valid['invalid']

    if not url_success:
        return jsonify({'message': 'No valid urls'}), 400

    if accuser_id == offender_id or offender_id == staff_id:
        return jsonify({'message': 'You cannot report yourself'}), 400

    conn = load_database()
    if not conn:
        abort(500, description='Failed to connect to database')

    cursor = conn.cursor(dictionary=True)

    query = '''
    INSERT INTO Report 
    (id, accuser_id, offender_id, staff_id, reason, report_date, report_time, server_id, bot, proof)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    try:
        if url_success:
            cursor.execute(query, (
                report_id,
                accuser_id,
                offender_id,
                staff_id,
                reason,
                report_date,
                report_time,
                server_id,
                int(bot),
                str(url_success),
            ))
            conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(500, description=f'Failed to insert report: {err}')
    finally:
        cursor.close()
        conn.close()

    if url_success and not (url_success_but or url_fails or url_invalid):
        return jsonify({
            'message': 'Report submitted successfully',
            'id': report_id,
        }), 200
    elif url_invalid or (url_fails and not url_success and not url_success_but):
        return jsonify({
            'message': 'Report cannot be made successfully as the proof URLs are invalid',
            'id': report_id
        }), 400
    else:
        return jsonify({
            'message': 'Report submitted successfully, but some URLs were invalid',
            'id': report_id,
        }), 422

@app.route('/api/v1/reports', methods=['GET'])
def all_reports():
    params = request.args
    if params:
        return jsonify({'message': 'This route does not accept parameters'}), 400

    conn = load_database()
    if not conn:
        abort(500, description='Failed to connect to the database')

    cursor = conn.cursor(dictionary=True)

    query = '''
    SELECT * FROM Report LIMIT 30
    '''
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()

        for row in resultado:
            for key, value in row.items():
                if isinstance(value, timedelta):
                    row[key] = str(value)

        return jsonify(resultado)
    except mysql.connector.Error as err:
        conn.rollback()
        abort(500, description=f'Failed to retrieve reports: {err}')
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

@app.errorhandler(429)
def rate_limit_error(error):
    ip = request.remote_addr
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.basicConfig(level=logging.DEBUG)
    logging.error(f'Rate limit exceeded: \nIP: {ip}\nTimestamp: {timestamp}')
    return jsonify({'message': 'Rate limit exceeded'}), 429

@app.errorhandler(500)
def internal_server_error(error):
    logging.basicConfig(level=logging.DEBUG)
    logging.error(f'Unexpected API Error: {error}')
    return jsonify({'message': 'Internal server error'}), 500



if __name__ == '__main__':
    run_project(app)
