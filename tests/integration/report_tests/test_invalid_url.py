import logging
from flask.testing import FlaskClient

def test_invalid_url(client:FlaskClient, url, succesReportData, createTokenRow):

    invalid_url = "urlInvalida"
    succesReportData["proof"] = invalid_url

    response = client.post(url,
                                    
        json = succesReportData,
        headers = {
            "Authorization": f"Bearer {createTokenRow}"
        }
    )
    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'The report could not be made because there are no valid URLs'
    assert response.status_code == 400