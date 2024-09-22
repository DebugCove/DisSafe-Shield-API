from extras.config import load_database
import mysql.connector


def token_validation(token, server_id):
    db = load_database()
    cursor = db.cursor()

    query = """
    SELECT token FROM tokens WHERE token = %s AND server_id = %s
    """

    cursor.execute(query, (token, server_id))
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False


token = "Put in the user token, not the discord token"
server_id = "Put the discord server id"

if token_validation(token, server_id):
    print("Valid Token!")
else:
    print("Invalid Token!")
