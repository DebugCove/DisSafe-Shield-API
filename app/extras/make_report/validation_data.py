import re

def validation_data(data):
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
        if isinstance(value, str):
            for pattern in dangerous_patterns:
                if re.search(pattern, value):
                    return {
                        'error': True,
                        'message': 'Invalid value entered',
                        'status_code': 400
                    }
        elif isinstance(value, (int, bool)):
            continue
        else:
            return {
                'error': True,
                'message': 'Invalid value entered',
                'status_code': 400
            }

    return {
        'error': False,
        'message': 'All values entered are valid',
        'status_code': 200
    }
