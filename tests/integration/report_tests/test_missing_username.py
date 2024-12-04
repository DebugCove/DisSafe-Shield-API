import logging
from flask.testing import FlaskClient

def test_missing_username(client:FlaskClient, url_prefix, succesReportData, createTokenRow):

    succesReportData.pop("staff_username")

    response = client.post(f"{url_prefix}/report",
                                    
        json = succesReportData,
        headers = {
            "Authorization": f"Bearer {createTokenRow}"
        }
    )
    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'Id or username not found'
    assert response.status_code == 400
