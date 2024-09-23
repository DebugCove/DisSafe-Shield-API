import os
import time
import logging
import requests
import validators
from random import randint
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv


def load_database(retries=3, delay=5):
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()
    db_config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "database": os.getenv("DB_DTB"),
    }
    if not isinstance(db_config, dict):
        raise ValueError("db_config must be a dictionary")

    for i in range(retries):
        try:
            conn = mysql.connector.connect(**db_config)
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("The database doesnt exist.")
            else:
                print(err)
            if i < retries - 1:
                print(f"Trying to reconnect in {delay} seconds...")
                time.sleep(delay)

    return None


def user_validation(id, username, status, timeout=5):
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    url = f"https://discord.com/api/v10/users/{id}"
    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return {"status_code": 599, "menssage": "Request timed out."}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"status_code": 404, "menssage": "User ID not found."}
        else:
            print(f"Error in verification: {e}")
            return {
                "status_code": response.status_code,
                "menssage": "Error in request.",
            }
    except requests.exceptions.RequestException as e:
        print(f"Error in verification: {e}")
        return {"status_code": 500, "menssage": "Internal Error Server"}

    user_data = response.json()
    actual_username = user_data["username"]

    if actual_username == username and status == "staff":
        return {"status_code": 200, "menssage": "Staff username and ID match."}
    elif actual_username == username and status == "user":
        return {"status_code": 200, "menssage": "Offender username and ID match."}
    elif actual_username != username and status == "staff":
        return {"status_code": 400, "menssage": "Staff username and ID don't match."}
    elif actual_username != username and status == "user":
        return {
            "status_code": 400,
            "menssage": "Offender username and ID do not match.",
        }


def url_validation(proof, timeout=5):
    success = []
    success_but = []
    fails = []
    invalid = []

    if not isinstance(proof, list):
        proof = proof.split(", ")

    for proofs in proof:
        if not validators.url(proofs):
            invalid.append(proofs)
            continue

        try:
            response = requests.get(proofs, timeout=timeout)
            if response.status_code == 200:
                success.append(proofs)
            else:
                success_but.append(proofs)
        except requests.exceptions.Timeout:
            fails.append(f"URL {proofs} cannot be reached -> Timeout")
        except requests.exceptions.RequestException as e:
            fails.append(f'The URL "{proofs}" cannot be reached -> ERROR: {e}')

    return {
        "success": success,
        "success_but": success_but,
        "fails": fails,
        "invalid": invalid,
    }


def unique_report_id_generator(retries=3, delay=5):
    db = load_database(retries, delay)
    cursor = db.cursor()
    cursor.execute("SELECT id FROM report")
    ids = cursor.fetchall()
    new_id = randint(1111111111111111, 9999999999999999)
    if new_id not in [row[0] for row in ids]:
        return new_id


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


def check_duplicates(banned_user_id, server_id):
    db = load_database()
    cursor = db.cursor()

    query = """
    SELECT banned_user_id FROM report WHERE banned_user_id = %s AND server_id = %s
    """

    cursor.execute(query, (banned_user_id, server_id))
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False
