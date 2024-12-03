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

    result = None

    logging.info("Has a test database")
    try:
        token = authTokenValue
        cursor = db.cursor()
        query = "INSERT INTO Tokens (token) VALUES (%s)"
        cursor.execute(query, (token,))

        nquery = 'SELECT token FROM Tokens WHERE token = %s'
        cursor.execute(nquery, (token,))
        result = cursor.fetchone()

    except mysql.connector.Error as err:
        logging.error(f"Token not created. Error: {err.msg}")
    
    assert result is not None
    yield result[0]
    

@pytest.fixture
def succesReportData():

    now = datetime.now()

    return {
        "id": "",
        "accuser_id": "",
        "accuser_username": "",
        "offender_id":"1",
        "staff_id": "",
        "staff_username": "",
        "reason": "",
        "report_date":now.strftime("%Y-%m-%d"),
        "report_time":now.strftime("%H:%M:%S"),
        "server_id":"1",
        "bot":"",
        "proof": "http://imgur.com/signin, http://flickr.com/about",
    }


@pytest.fixture
def reportRow(db, succesReportData):
    
    logging.info("Has a test database")

    result = None
    
    try:

        accuser_username = succesReportData.pop("accuser_username")
        staff_username = succesReportData.pop("staff_username")
            
        cursor = db.cursor()
        query = """INSERT INTO Report 
            (id, accuser_id, offender_id, staff_id, reason, report_date, report_time, bot, proof) 
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(query, tuple(succesReportData.values()))

        nquery = """SELECT * FROM Report WHERE
            id=%s, accuser_id=%s, offender_id=%s, staff_id=%s, reason=%s, report_date=%s, 
            report_time=%s, bot=%s, proof=%s"""
        
        cursor.execute(nquery, tuple(succesReportData.values()))
        result = cursor.fetchone()

        succesReportData["accuser_username"] = accuser_username
        succesReportData["staff_username"] = staff_username

    except mysql.connector.Error as err:
        logging.error(f"Report not created. Error: {err.msg}")

    assert result is not None
    yield None