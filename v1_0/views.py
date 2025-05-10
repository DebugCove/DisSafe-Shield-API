import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache
from .extras.auth_verification import auth_verf
from .extras.entry_verification import entry_validation
from .extras.info_generator import generate_date, generate_time
from .extras.make_report.missing_data import missing_data
from .extras.make_report.proof_validation import proof_validation
from .extras.make_report.id_generator import id_generator
from .extras.make_report.send_database import send_database


@never_cache
def index_view(request):
    if request.method == 'OPTIONS':
        response = HttpResponse(status=204)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    elif request.method == 'GET':
        return JsonResponse({"message": "DisSafe Shield API"})
    else:
        return JsonResponse({'message': 'Method invalid'}, status=405)


@never_cache
def status_view(request):
    if request.method == 'OPTIONS':
        response = HttpResponse(status=204)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    elif request.method == 'GET':
        return JsonResponse({'message': 'Status Ok'})
    else:
        return JsonResponse({'message': 'Method invalid'}, status=405)


@never_cache
def make_report_view(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Method invalid'}, status=405)

    token = request.headers.get('Authorization')
    result = auth_verf(token, route='make_report')

    if result['error']:
        if 400 <= result['status_code'] < 500:
            return JsonResponse({'message': result['message']}, status=result['status_code'])
        return JsonResponse({'message': 'Internal authentication error'}, status=500)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'message': 'Internal authentication error'}, status=500)

    result = missing_data(data)
    if result['error']:
        if 400 <= result['status_code'] < 500:
            return JsonResponse({'message': result['message']}, status=result['status_code'])
        return JsonResponse({'message': 'Internal authentication error'}, status=500)

    result = entry_validation(data)
    if result['error']:
        if 400 <= result['status_code'] < 500:
            return JsonResponse({'message': result['message']}, status=result['status_code'])
        return JsonResponse({'message': 'Internal authentication error'}, status=500)

    result = proof_validation(data)
    if result['error']:
        if 400 <= result['status_code'] < 500:
            return JsonResponse({'message': result['message']}, status=result['status_code'])
        return JsonResponse({'message': 'Internal authentication error'}, status=500)
    data['proof'] = []
    proof_list = result['data']['success'] + result['data']['success_but']
    data['proof'] = ' '.join(proof_list)

    data['id'] = id_generator()['data']['id']
    data['date'] = generate_date()
    data['time'] = generate_time()

    result = send_database(data)
    if result['error']:
        if 400 <= result['status_code'] < 500:
            return JsonResponse({'message': result['message']}, status=result['status_code'])
        return JsonResponse({'message': 'Internal authentication error'}, status=500)
    return JsonResponse({'message': 'Report created successfully'}, status=200)