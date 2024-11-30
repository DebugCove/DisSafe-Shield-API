import mysql.connector
import pytest
import logging
import mysql.connector
from datetime import datetime
import secrets

@pytest.fixture
def authTokenValue():
    return secrets.token_urlsafe(16)


@pytest.fixture
def url_prefix():
    return "/api/v1"


@pytest.fixture
def createTokenRow(db, authTokenValue):

    if db:
        logging.info("Has a test database")
        try:
            token = authTokenValue
            cursor = db.cursor()
            query = "INSERT INTO Tokens (token) VALUES (%s)"
            cursor.execute(query, (token,))

            nquery = 'SELECT * FROM Tokens WHERE token = %s'
            cursor.execute(nquery, (token,))
            result = cursor.fetchone()

            if not result:
                return None

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
        "offender_id":"1",
        "staff_id": "",
        "staff_username": "",
        "reason": "",
        "report_date":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "report_time":"",
        "server_id":"1",
        "bot":"",
        "proof": "http://imgur.com, http://flickr.com",
    }


@pytest.fixture
def reportRow(db, succesReportData):
    
    if db:
        logging.info("Has a test database")

        try:
            keys = "id, accuser_id, offender_id, staff_id, reason, report_date, report_time, bot, proof"
            splited_keys = keys.split(", ")
            values = ""
            for key in splited_keys:
                values += f"{succesReportData[key]},"
            values = values[:-1]
            
            cursor = db.cursor()
            query = "INSERT INTO Report (%s) VALUES (%s)"
            cursor.execute(query, (keys, values))

            logging.info("Report created")

            return succesReportData

        except mysql.connector.Error as err:
            logging.error(f"Report not created. Error: {err.msg}")
            return None
    else:
        logging.error("Hasn't a test database")
        return None
