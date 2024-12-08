from flask.testing import FlaskClient

def test_invalid_token_format(client:FlaskClient, url, succesReportData):

    response = client.post(url,
        json = succesReportData,
        headers = {
            "Authorization": "Bearer "
        }
    )

    json = response.get_json()
    assert json
    res = json["message"]
    assert res ==  'Not valid token format'
    assert response.status_code == 400