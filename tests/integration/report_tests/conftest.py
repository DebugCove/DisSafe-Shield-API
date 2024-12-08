import mysql.connector
import pytest
import logging
import mysql.connector
from datetime import datetime
import secrets

@pytest.fixture(scope="session")
def authTokenValue():
    return secrets.token_urlsafe(16)


@pytest.fixture(scope="session")
def url():
    return "/api/v1/report"


@pytest.fixture(scope="session")
def createTokenRow(db, authTokenValue):
    
    result = None

    logging.info("Has a test database")
    try:
        token = authTokenValue
        cursor = db.cursor()
        query = "INSERT INTO Tokens (token) VALUES (%s)"
        cursor.execute(query, (token,))
        db.commit()

        nquery = 'SELECT token FROM Tokens WHERE token = %s'
        cursor.execute(nquery, (token,))
        result = cursor.fetchone()

    except mysql.connector.Error as err:
        logging.error(f"Token not created. Error: {err.msg}")
    
    assert result is not None
    return result[0]
    

@pytest.fixture
def succesReportData():

    now = datetime.now()

    return {
        "id": 1232432,
        "accuser_id": 457943440387342336,
        "accuser_username": "jrgames1234",
        "offender_id": 395546295940415510,
        "offender_username":"shauuu_",
        "staff_id": 599243713448771585,
        "staff_username": "lucasgomes220418",
        "reason": "anyreason",
        "report_date": now.strftime("%Y-%m-%d"),
        "report_time": now.strftime("%H:%M:%S"),
        "server_id": 1245457789653094531,
        "bot": "anybot",
        "proof": "http://imgur.com/signin, http://flickr.com/about",
    }


@pytest.fixture
def reportRow(db, succesReportData):
    
    logging.info("Has a test database")

    result = None
    
    try:

        id = succesReportData['id']
        accuser_id = succesReportData['accuser_id']
        offender_id = succesReportData['offender_id']
        staff_id = succesReportData['staff_id']
        reason = succesReportData['reason']
        report_date = succesReportData['report_date']
        report_time = succesReportData['report_time']
        bot = succesReportData['bot']
        proof = succesReportData['proof']
            
        cursor = db.cursor()
        query = """INSERT INTO Report 
            (id, accuser_id, offender_id, staff_id, reason, report_date, report_time, bot, proof) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(query, (
            id, accuser_id, offender_id, staff_id, reason, report_date, report_time, bot, proof
        ))

        nquery = """SELECT * FROM Report WHERE
            id=%s AND accuser_id=%s AND offender_id=%s AND staff_id=%s AND reason=%s AND report_date=%s AND 
            report_time=%s AND bot=%s AND proof=%s"""
        
        cursor.execute(nquery, (
            id, accuser_id, offender_id, staff_id, reason, report_date, report_time, bot, proof
        ))

        result = cursor.fetchone()[0]


    except mysql.connector.Error as err:
        logging.error(f"Report not created. Error: {err.msg}")

    assert result is not None
    return None