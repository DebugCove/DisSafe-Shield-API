import logging
from flask.testing import FlaskClient

def test_not_allowed_url(client:FlaskClient, url, succesReportData, createTokenRow):

    proof_url = "http://youtube.com"
    succesReportData["proof"] = proof_url

    response = client.post(url,
                                    
        json = succesReportData,
        headers = {
            "Authorization": f"Bearer {createTokenRow}"
        }
    )
    json = response.get_json()
    res = json["message"]
    assert res == 'Report was completed successfully, but some links were not included.'
    assert response.status_code == 400
