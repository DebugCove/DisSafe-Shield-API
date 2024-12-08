import logging
from flask.testing import FlaskClient


def test_invalid_username(client:FlaskClient, url, succesReportData, createTokenRow):

    succesReportData["staff_username"] = "other"

    response = client.post(url,
                                    
        json = succesReportData,
        headers = {
            "Authorization": f"Bearer {createTokenRow}"
        }
    )
    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'Staff username not match with id '
    assert response.status_code == 400