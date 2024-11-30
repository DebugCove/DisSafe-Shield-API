from flask.testing import FlaskClient

def test(client:FlaskClient, url_prefix, succesReportData):

    response = client.post(f"{url_prefix}/report",
                                    
        json = succesReportData,
        headers = {
            "Authorization": f"Bearer any"
        }
    )
    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'Token is invalid'
    assert response.status_code == 401