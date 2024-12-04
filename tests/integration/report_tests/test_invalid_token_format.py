from flask.testing import FlaskClient

def test_invalid_token_format(client:FlaskClient, url_prefix, succesReportData):

    response = client.post(f"{url_prefix}/report",
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