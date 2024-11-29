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
def succesReportData():
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

def test_succes_report(client:FlaskClient, succesReportData, createTokenRow):
    logging.info("Succes report route test started")

    if createTokenRow:
        response = client.post("/report",
                                    
            data = succesReportData,
            headers = {
                "Authorization": f"Bearer {createTokenRow}"
            }
        )
        res = json.loads(response.data.decode('utf-8')).get("message")
        assert response.status_code == 200
        assert res == 'Report sent successfully.'
    else:
        logging.error("Test Failed. Reason: hasn't token.")


def test_report_missing_data(client:FlaskClient):
    logging.info("Report route test missing data started")

    response = client.post("/report")

    res = json.loads(response.data.decode('utf-8')).get("message")
    assert response.status_code == 400
    assert res == 'Data not defined'


def test_report_missing_auth_header(client:FlaskClient, succesReportData)
    logging.info("Report route test missing auth header started")

    response = client.post("/report",
            data = succesReportData
    )

    res = json.loads(response.data.decode('utf-8')).get("message")
    assert response.status_code == 401
    assert res == 'Token not provided or invalid'


def test_report_missing_offender_id(client:FlaskClient, succesReportData, createTokenRow)

    succesReportData.pop("accuser_id")

    if createTokenRow:
        response = client.post("/report",
                                    
            data = succesReportData,
            headers = {
                "Authorization": f"Bearer {createTokenRow}"
            }
        )
        res = json.loads(response.data.decode('utf-8')).get("message")
        assert response.status_code == 400
        assert res == 'offender_id or server_id were not provided.'
    else:
        logging.error("Test Failed. Reason: hasn't token.")
    

