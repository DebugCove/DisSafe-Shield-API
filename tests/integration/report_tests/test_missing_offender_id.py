import logging
from flask.testing import FlaskClient

def test(client:FlaskClient, url_prefix, succesReportData, createTokenRow):

    succesReportData.pop("offender_id")

    response = client.post(f"{url_prefix}/report",
                                    
        json = succesReportData,
        headers = {
            "Authorization": f"Bearer {createTokenRow}"
        }
    )
    
    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'offender_id or server_id were not provided.'
    assert response.status_code == 400