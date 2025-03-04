import validators
import requests
from urllib.parse import urlparse


def proof_validation(data):
    allowed_domains = {
        'imgur.com', 'flic.kr', '1drv.ms', 'photos.app.goo.gl', 'drive.google.com', 
        'icloud.com', 'mega.nz', 'dropbox.com', 'imagizer.imageshack.com'
    }

    results = {
        'success': [],
        'success_but': [], 
        'fails': [],
        'invalid': [],
        'not_allowed_domains': []
    }

    proof = data.get('proof')

    if not proof:
        print('Proof is missing or empty')
        return {
            'error': True,
            'message': 'Proof is missing or empty',
            'status_code': 400
        }
    
    if isinstance(proof, str):
        proof = proof.split()
    elif not isinstance(proof, list):
        print('Invalid proof format')
        return {
            'error': True,
            'message': 'Invalid proof format; expected list or space-separated string',
            'status_code': 400
        }

    for url in proof:
        if not isinstance(url, str) or not validators.url(url):
            print(f'{url} is invalid or not a string')
            results['invalid'].append(url)
            continue

        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        if not any(domain.endswith(allowed) for allowed in allowed_domains):
            print(f'{url} does not have a dominance or does not end up with domain that is in the allowed list')
            results['not_allowed_domains'].append(domain)
            continue

        try:
            print(f'Make request for {url}')
            response = requests.get(url, timeout=5)
            if response.status_code in range(200, 300):
                print(f'{url} gave the result of {response.status_code}')
                results['success'].append(url)
            else:
                print(f'{url} gave the result of {response.status_code}')
                results['fails'].append(url)
        except requests.RequestException as error:
            print(f'{url} gave a mistake when making the remake {error}')
            results['fails'].append(url)

    if not results['success']:
        return {
            'error': True,
            'message': 'No valid URLs were found',
            'status_code': 400
        }

    return {
        'error': False,
        'message': 'All URLs have been processed',
        'status_code': 200,
        'data': results
    }
