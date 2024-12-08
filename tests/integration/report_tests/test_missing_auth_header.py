import logging
from flask.testing import FlaskClient

def test_missing_auth_header(client:FlaskClient, url, succesReportData):
    logging.info("Report route test missing auth header started")

    response = client.post(url,
        json = succesReportData
    )

    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'Token not provided or invalid'
    assert response.status_code == 401