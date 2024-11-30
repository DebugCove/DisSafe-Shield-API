import logging
from flask.testing import FlaskClient

def test(client:FlaskClient, url_prefix, succesReportData):
    logging.info("Report route test missing auth header started")

    response = client.post(f"{url_prefix}/report",
        json = succesReportData
    )

    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'Token not provided or invalid'
    assert response.status_code == 401