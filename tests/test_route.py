import mysql.connector
import pytest
import logging
import mysql.connector
from mysql.connector import errorcode
from flask.testing import FlaskClient
import secrets

@pytest.fixture
def authTokenValue():
    return secrets.token_urlsafe(16)


@pytest.fixture
def createTokenRow(db, authTokenValue):

    if db:
        logging.info("Has a test database")
        try:
            token = authTokenValue
            cursor = db.cursor()
            query = "INSERT INTO Tokens (token) VALUES (%s)"
            cursor.execute(query, (token,))

            logging.info("Token created")

            return authTokenValue

        except mysql.connector.Error as err:
            logging.error(f"Token not created. Error: {err.msg}")
            return None
    else:
        logging.error("Hasn't a  test database")
        return None


@pytest.fixture
def succesData():
    return {
        "id": "",
        "accuser_id": "",
        "accuser_username": "",
        "staff_id": "",
        "staff_username": "",
        "reason": "",
        "report_date":"",
        "report_time":"",
        "server_id":"",
        "bot":"",
        "proof": "http://imgur.com, http://flickr.com",
    }

def test_succes_report(self, client:FlaskClient, succesData, createTokenRow):
    logging.info("Report route test started")

    if createTokenRow:
        logging.info("Starting request")
        response = client.post("/report",
                                    
            data = succesData,
            headers = {
                "Authorization": f"Bearer {authTokenValue}"
            }
        )

        assert response.status_code == 200
    else:
        logging.error("Test Failed. Reason: hasn't token.")

