import re


def entry_validation(data):
    if not data:
        return {
            'error': True,
            'message': 'Data is None',
            'status_code': 401
        }

    dangerous_patterns = [
        r'<.*?>',
        r'<\?php.*?\?>',
        r'(?i)script',
        r'(?i)on\w+\s*=\s*',
        r'(?i)document\.',
        r'(?i)window\.',
        r'(?i)eval\(',
        r'(?i)alert\(',
        r'(?i)innerHTML',
        r'(?i)setTimeout\(',
        r'(?i)setInterval\(',
        r'(?i)fetch\(',
        r'(?i)XMLHttpRequest',
        r'(?i)select\s.*?from',
        r'(?i)union\s.*?select',
        r'(?i)insert\sinto',
        r'(?i)delete\s+from',
        r'(?i)update\s+.*?\s+set',
        r'(?i)drop\s.*?table',
        r'(?i)exec\s',
        r'(?i)xp_cmdshell',
        r'(?i)sp_executesql',
        r'(?i)--',  
        r'(?i)\bOR\b.*=\s*\bOR\b',  
        r'(?i);\s*sh\s*-c',
        r'(?i);\s*rm\s+-rf',
        r'(?i);\s*wget\s+',
        r'(?i);\s*curl\s+',
        r'(?i);\s*nc\s+-e',
        r'(?i);\s*cat\s+/etc/passwd',
        r'(?i)python\s+-c',
        r'(?i)bash\s+-c',
        r'%00',  
        r'0x[0-9A-Fa-f]+',  
    ]

    for key, value in data.items():
        if value is None:
            return {
                'error': True,
                'message': f'Value for "{key}" is None',
                'status_code': 401
            }

        if isinstance(value, str):
            if any(re.search(pattern, value) for pattern in dangerous_patterns):
                return {
                    'error': True,
                    'message': f'Invalid value detected in "{key}"',
                    'status_code': 401
                }
        elif not isinstance(value, (int, bool)):
            return {
                'error': True,
                'message': f'Invalid type for "{key}"',
                'status_code': 401
            }

    return {
        'error': False,
        'message': 'All values entered are valid',
        'status_code': 200
    }
