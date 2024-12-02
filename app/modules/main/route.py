from flask import Blueprint, jsonify, request
from ...extras.report.user_validation import user_validation
from ...extras.report.token_validation import token_validation
from ...extras.report.proof_validation import proof_validation
from ...extras.report.id_report_generator import report_id_generator
from ...extras.report.check_duplicates import check_duplicates


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

    result_check_duplicates = check_duplicates(data)
    if result_check_duplicates['error']:
        return jsonify({'message': result_check_duplicates['message']}), result_check_duplicates['status_code']

    result_data_validation = user_validation(data, status='staff')
    if result_data_validation['error']:
        return jsonify({'message': result_data_validation['message']}), result_data_validation['status_code']

    result_data_validation = user_validation(data, status='user')
    if result_data_validation['error']:
        return jsonify({'message': result_data_validation['message']}), result_data_validation['status_code']

    result_proof_validation = proof_validation(data)
    error_proof_validation = result_proof_validation['error']
    data_result_proof_validation = result_proof_validation['data'][0]['success']
    data['proof'] = data_result_proof_validation

    result_id_generator = report_id_generator()
    if result_id_generator['error']:
        return jsonify({'message': result_id_generator['message']}), result_id_generator['status_code']
    data['id'] = result_id_generator


    if error_proof_validation:
        return jsonify({'message': 'Report was completed successfully, but some links were not included.'}), 200
    else:
        return jsonify({'message': 'Report sent successfully.'}), 200
