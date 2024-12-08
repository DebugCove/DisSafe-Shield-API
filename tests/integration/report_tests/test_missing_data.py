import logging
from flask.testing import FlaskClient

def test_missing_data(client:FlaskClient, url, succesReportData, createTokenRow):
    logging.info("Report route test missing data started")

    missing_field = 'accuser_username'

    succesReportData.pop(missing_field)

    response = client.post(url,
        json = succesReportData,
        headers = {
            "Authorization": f"Bearer {createTokenRow}"
        }
    )

    json = response.get_json()
    assert json
    res = json["message"]
    assert res == f'Missing required fields:{missing_field}'
    assert response.status_code == 400