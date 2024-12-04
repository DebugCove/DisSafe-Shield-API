import logging
import validators
import requests
from urllib.parse import urlparse

def proof_validation(data):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nProof Validation')

    allowed_domains = [
        'imgur.com', 'flickr.com', 'photos.google.com', 'dropbox.com', 
        '500px.com', 'imageshack.com', 'photobucket.com', 
        'unsplash.com', 'onedrive.live.com', 'drive.google.com', 
        'icloud.com', 'mega.nz', '1drv.ms'
    ]

    success = []
    success_but = []
    fails = []
    invalid = []
    not_allowed_domains = []

    proof = data.get('proof')
    if proof is None:
        return {
            'error': True,
            'message': 'Proof is not defined',
            'status_code': 400
        }

    if isinstance(proof, str):
        proof = proof.split()

    for url in proof:
        logging.info('Check the URL: %s', url)

        if not isinstance(url, str) or not validators.url(url):
            logging.error('Invalid URL: %s', url)
            invalid.append(url)
            url.pop(url)
            continue

        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if not any(domain.endswith(allowed_domain) for allowed_domain in allowed_domains):
            logging.error('URL: %s is not in allowed domains', url)
            not_allowed_domains.append(url)
            url.pop(url)
            continue

        try:
            response = requests.get(url, timeout=5)
            if response.status_code in range(200, 299):
                success.append(url)
            else:
                success_but.append(url)
        except requests.exceptions.RequestException as e:
            logging.error('Error: %s', e)
            fails.append(url)

    if fails or invalid or not_allowed_domains or success_but:
        if not success:
            return {
                'error': True,
                'message': 'The report could not be made because there are no valid URLs',
                'status_code': 400
            }
        return {
            'error': True,
            'message': 'All the URLs have been checked, but there are some URLs that are invalid, have problems, or are not allowed.',
            'status_code': 400,
            'data': {
                'success': success,
                'success_but': success_but,
                'fails': fails,
                'invalid': invalid,
                'not_allowed_domains': not_allowed_domains,
            }
        }

    return {
        'error': False,
        'message': 'All URLs were checked without errors',
        'status_code': 200,
        'data': {
            'success': success,
        }
    }
