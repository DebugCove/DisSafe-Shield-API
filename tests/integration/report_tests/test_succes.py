import logging
from flask.testing import FlaskClient

def test_succes(client:FlaskClient, url, succesReportData, createTokenRow):
    logging.info("Succes report route test started")

    response = client.post(url,
                                    
        json = succesReportData,
        headers = {
            "Authorization": f"Bearer {createTokenRow}"
        }
    )
    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'Report sent successfully.'
    assert response.status_code == 200
    