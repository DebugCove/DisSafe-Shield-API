from flask import Blueprint, jsonify, request
from ...extras.user_validation import user_validation
from ...extras.token_validation import token_validation


main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    params = request.args
    if params:
        return jsonify({'message': 'The route does accept parameters'}), 400
    else:
        return jsonify({'message': 'DisSafe API running'})

@main_bp.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok'})

@main_bp.route('/report', methods=['POST'])
def make_report():
    data = request.get_json()
    auth_header = request.headers.get('Authorization')
    result_token_validation = token_validation(data, auth_header)
    if result_token_validation['error']:
        return jsonify({'message': result_token_validation['message']}), result_token_validation['status_code']

    result_data_validation = user_validation(data, status='staff')
    if result_data_validation['error']:
        return jsonify({'message': result_data_validation['message']}), result_data_validation['status_code']

    result_data_validation = user_validation(data, status='user')
    if result_data_validation['error']:
        return jsonify({'message': result_data_validation['message']}), result_data_validation['status_code']

    return jsonify({'message': 'Report sent successfully'}), 200
