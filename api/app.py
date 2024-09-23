import os
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request, jsonify, redirect, abort
from flask_talisman import Talisman
from extras.config import load_database, user_validation, url_validation, unique_report_id_generator, token_validation, check_duplicates


app = Flask(__name__)
app.secret_key = os.urandom(24)


Talisman(
    app,
    frame_options='DENY',  # X-Frame-Options: Prevents the page from being embedded in an iframe
    x_xss_protection=True,  # X-XSS-Protection: Enables XSS protection
    strict_transport_security=True,  # Strict-Transport-Security (HSTS): Forces HTTPS
    strict_transport_security_max_age=31536000  # Sets HSTS max age to 1 year
)


@app.route('/', methods=['GET'])
def index():
    params = request.args
    if params:
        return jsonify({'message': 'This route does not accept parameters'}), 400
    else:
        return redirect('api'), 308


@app.route('/api/v1', methods=['GET'])
def api():
    params = request.args
    if params:
        return jsonify({'message': 'This route does not accept parameters'}), 400
    else:
        return jsonify({'message': 'DisSafe Shield API'}), 200


@app.route('/api/v1/report', methods=['POST'])
def report():
    params = request.args
    if params:
        return jsonify({'message': 'This route does not accept parameters'}), 400

    data = request.get_json()
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Token not provided or invalid'}), 401

    token = auth_header.split(" ")[1]
    required_fields = ['staff_username', 'staff_id', 'banned_user', 'banned_user_id', 'reason', 'server_id', 'bot', 'proof']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return abort(400, description=f"Missing required fields: {', '.join(missing_fields)}")

    server_id = data.get('server_id')
    if not token_validation(token, server_id):
        return jsonify({'message': 'Token not provided or valid'}), 401
    report_id = unique_report_id_generator()


    staff_username = data.get('staff_username')
    staff_id = data.get('staff_id')
    status = "staff"
    validation = user_validation(staff_id, staff_username, status=status)
    if validation['status_code'] != 200:
        message = validation['message']
        status_code = validation['status_code']
        return jsonify({'message': message}), status_code


    banned_user = data.get('banned_user')
    banned_user_id = data.get('banned_user_id')
    status = "user"
    validation = user_validation(banned_user_id, banned_user, status=status)
    if validation['status_code'] != 200:
        message = validation['message']
        status_code = validation['status_code']
        return jsonify({'message': message}), status_code

    result_of_duplicates = check_duplicates(banned_user_id, server_id)
    if result_of_duplicates:
        return jsonify({'message': 'You have already reported this user'}), 400

    reason = data.get('reason')
    if not isinstance(reason, str):
        return jsonify({'message': 'Reason not valid'}), 400

    current_date = datetime.now()
    date = current_date.strftime('%Y-%m-%d')  # Format: YEAR-MONTH-DAY
    time = current_date.strftime('%H:%M:%S')  # Format: HOUR:MINUTE:SECONDS

    bot = data.get('bot')
    if bot not in [0, 1, True, False]:
        return jsonify({'message': 'Bot not valid'}), 400

    proof = data.get('proof')
    url_valid = url_validation(proof)
    url_success = url_valid['success']
    url_success_but = url_valid['success_but']
    url_fails = url_valid['fails']
    url_invalid = url_valid['invalid']

    if staff_username == banned_user or staff_id == banned_user_id:
        return jsonify({'message': 'You cannot report yourself'}), 400

    conn = load_database()
    if not conn:
        abort(500, description='Failed to connect to database')

    cursor = conn.cursor(dictionary=True)

    query = '''
    INSERT INTO report 
    (id, staff_username, staff_id, banned_user, banned_user_id, reason, date, time, server_id, bot, proof)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    try:
        if url_success:
            cursor.execute(query,
                (
                    report_id,
                    staff_username,
                    staff_id,
                    banned_user,
                    banned_user_id,
                    reason,
                    date,
                    time,
                    server_id,
                    bot,
                    str(url_success),
                ),
            )
            conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        abort(500, description=f'Failed to insert report: {err}')
    finally:
        cursor.close()
        conn.close()


    if url_success and not (url_success_but or url_fails or url_invalid):
        return jsonify({'message': 'Report submitted successfully'}), 200

    elif url_invalid or url_fails and not url_success and not url_success_but:
        return jsonify({'message': 'Report cannot be made successfully as the proof URLs are invalid'}), 400

    else:
        return jsonify({
            'message': 'Report submitted successfully, but some URLs were invalid',
            'success': url_success,
            'success_but': url_success_but,
            'fails': url_fails,
            'invalid': url_invalid
        }), 422






if __name__ == '__main__':
    load_dotenv()
    PORT = os.getenv('FLASK_PORT')
    DEBUG = os.getenv('FLASK_DEBUG')
    app.run(host='0.0.0.0', debug=DEBUG, port=PORT)
