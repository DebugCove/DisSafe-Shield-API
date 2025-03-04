import json
from ..database.make_connection import connect_database


def get_route_info(route):
    """
    Fetches route information from the database based on the given route.

    Args:
        route (str): The route identifier to look up in the database.

    Returns:
        dict: A dictionary containing the results of the query with keys:
            - 'error' (bool): Indicates if there was an error.
            - 'message' (str): A message describing the result or error.
            - 'status_code' (int): HTTP-like status code indicating success or failure.
            - 'data' (optional, str): JSON string of the route information if successful.
    """

    print('Get route info')
    query = 'SELECT * FROM Route_info WHERE route = %s'

    if route is None:
        return {
            'error': True,
            'message': 'Route is not defined',
            'status_code': 500
        }

    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(query, (route,))
        column = [desc[0] for desc in cursor.description]

        result = cursor.fetchall()

        if result is None:
            return {
                'error': True,
                'message': 'Route not found',
                'status_code': 500
            }
        return {
            'error': False,
            'message': 'Route found',
            'status_code': 200,
            'data': result
        }
    except Exception as error:
        return {
            'error': True,
            'message': f'Database error {str(error)}',
            'status_code': 500,
        }


def get_token_info(auth):
    """
    Fetches token information from the database based on the given Bearer token.

    Args:
        auth (str): The Bearer token to look up in the database.

    Returns:
        dict: A dictionary containing the results of the query with keys:
            - 'error' (bool): Indicates if there was an error.
            - 'message' (str): A message describing the result or error.
            - 'status_code' (int): HTTP-like status code indicating success or failure.
            - 'data' (optional, str): JSON string of the token information if successful.
    """
    print('Get Token Info')
    query = 'SELECT * FROM Tokens WHERE token = %s'

    if not auth.startswith('Bearer '):
        return {
            'error': True,
            'message': 'Invalid token format. Use Bearer <token>.',
            'status_code': 401
        }

    token = auth[7:]

    if not token:
        return {
            'error': True,
            'message': 'Token is empty.',
            'status_code': 401
        }

    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(query, (token,))
        column = [desc[0] for desc in cursor.description]

        result = cursor.fetchall()

        if result is None:
            return {
                'error': True,
                'message': 'Token not found',
                'status_code': 400
            }
        return {
            'error': False,
            'message': 'Token found',
            'status_code': 200,
            'data': result
        }
    except Exception as error:
        return {
            'error': True,
            'message': f'Database error: {str(error)}',
            'status_code': 500
        }


def auth_verf(auth, route):
    """
    Verifies the given authentication token against the given route.

    Args:
        auth (str): The Bearer token to verify.
        route (str): The route identifier to check the token against.

    Returns:
        dict: A dictionary containing the results of the verification with keys:
            - 'error' (bool): Indicates if there was an error.
            - 'message' (str): A message describing the result or error.
            - 'status_code' (int): HTTP-like status code indicating success or failure.
    """
    if not auth:
        return {
            'error': True,
            'message': 'Authentication is required. Please provide a valid API key.',
            'status_code': 401
        }

    token_info = get_token_info(auth)
    if token_info['error']:
        return token_info
    route_info = get_route_info(route)
    if route_info['error']:
        return route_info

    if int(token_info['data'][0][-1]) >= int(route_info['data'][0][-1]):
        return {
            'error': False,
            'message': 'Token verified successfully',
            'status_code': 200
        }
    else:
        return {
            'error': True,
            'message': 'Token does not have permission for the route',
            'status_code': 400
        }
