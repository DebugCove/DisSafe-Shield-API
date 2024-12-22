from flask import Blueprint, jsonify, request

from app.extras.make_report.user_validation import user_validation
from app.extras.make_report.proof_validation import proof_validation
from app.extras.make_report.id_report_generator import report_id_generator
from app.extras.make_report.check_duplicates import check_duplicates
from app.extras.make_report.request_database import request_database
from app.extras.make_report.missing_data import missing_data
from app.extras.make_report.validation_data import validation_data
from app.extras.view_report.get_info import get_info_report
from app.extras.token_validation import token_validation
from app.extras.info_generator import generate_date
from app.extras.info_generator import generate_hour


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
    result_token_validation = token_validation(auth_header)
    if result_token_validation['error']:
        return jsonify({'message': result_token_validation['message']}), result_token_validation['status_code']

    result_validation_data = validation_data(data)
    if result_validation_data['error']:
        return jsonify({'message': result_validation_data['message']}), result_validation_data['status_code']

    result_missing_data = missing_data(data)
    if result_missing_data['error']:
        return jsonify({'message': result_missing_data['message']}), result_missing_data['status_code']

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
    if error_proof_validation:
        return jsonify({'message': result_proof_validation['message']}), result_proof_validation['status_code']
    successful_urls = result_proof_validation['data']['success']
    success_but_urls = result_proof_validation['data']['success_but']
    fails_urls = result_proof_validation['data']['fails']
    invalid_urls = result_proof_validation['data']['invalid']
    not_allowed_domains = result_proof_validation['data']['not_allowed_domains']
    data['proof'] = successful_urls

    result_id_generator = report_id_generator()
    if result_id_generator['error']:
        return jsonify({'message': result_id_generator['message']}), result_id_generator['status_code']
    data['id'] = result_id_generator['data']['id']
    data['report_date'] = generate_date()
    data['report_time'] = generate_hour()

    result_request_database = request_database(data)
    if result_request_database['error']:
        return jsonify({'message': result_request_database['message']}), result_request_database['status_code']

    if success_but_urls or fails_urls or invalid_urls or not_allowed_domains:
        return jsonify({'message': 'Report was completed successfully, but some links were not included.'}), 200
    else:
        return jsonify({'message': 'Report sent successfully.'}), 200

@main_bp.route('/view_report', methods=['GET'])
def view_report():
    auth_header = request.headers.get('Authorization')
    result_token_validation = token_validation(auth_header)
    if result_token_validation['error']:
        return jsonify({'message': result_token_validation['message']}), result_token_validation['status_code']

    id = request.args.get('id', type=str)
    if id is None:
        return jsonify({'message': 'ID is not found'})

    result_info_report = get_info_report(id)
    if result_info_report['error']:
        return jsonify({'message': result_info_report['message']}), result_info_report['status_code']

    return jsonify({
        'message': result_info_report['message'], 
        'data': result_info_report['data']}), result_info_report['status_code']
