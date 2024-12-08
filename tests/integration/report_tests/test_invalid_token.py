from flask.testing import FlaskClient

def test_invalid_token(client:FlaskClient, url, succesReportData):

    response = client.post(url,
                                    
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