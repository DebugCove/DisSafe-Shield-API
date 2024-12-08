import logging
from flask.testing import FlaskClient

def test_existing_report(client:FlaskClient, url, succesReportData, createTokenRow, reportRow):

    response = client.post(url,
                                    
        json = succesReportData,
        headers = {
            "Authorization": f"Bearer {createTokenRow}"
        }
    )
    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'Report is duplicate'
    assert response.status_code == 400