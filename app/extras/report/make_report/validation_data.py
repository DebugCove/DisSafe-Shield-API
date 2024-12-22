import re
import logging


def validation_data(data):
    logging.basicConfig(level=logging.DEBUG)
    logging.info('\n\nValidate the report date\n')

    if not data:
        logging.error('Data is not defined')
        return {
            'error': True,
            'message': 'Data is not defined',
            'status_code': 400
        }

    dangerous_patterns = [
        r"<.*?>", 
        r"<\?php.*?\?>",
        r"(?i)script", 
        r"(?i)on\w+\s*=",  
        r"(?i)select\s.*?from",  
        r"(?i)union\s.*?select", 
        r"(?i)insert\sinto",  
        r"(?i)drop\s.*?table",  
        r"(?i)--",  
        r"(?i)eval\(", 
        r"(?i)alert\(", 
        r"(?i)document\.",  
        r"(?i)window\.",
    ]

    for key, value in data.items():
        if value is None:
            logging.error('Null pointer reference')
            return {
                'error': True,
                'message': 'Data is not defined',
                'status_code': 400
            }

        if isinstance(value, str):
            for pattern in dangerous_patterns:
                if re.search(pattern, value):
                    logging.error('Invalid value entered')
                    return {
                        'error': True,
                        'message': 'Invalid value entered',
                        'status_code': 400
                    }
        elif isinstance(value, (int, bool)):
            continue
        else:
            logging.error('Invalid value entered')
            return {
                'error': True,
                'message': 'Invalid value entered',
                'status_code': 400
            }

    logging.info('All values entered are valid')
    return {
        'error': False,
        'message': 'All values entered are valid',
        'status_code': 200
    }
