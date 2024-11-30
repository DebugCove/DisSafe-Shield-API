import logging
from flask.testing import FlaskClient

def test(client:FlaskClient, url_prefix):
    logging.info("Report route test missing data started")

    response = client.post(f"{url_prefix}/report")

    json = response.get_json()
    assert json
    res = json["message"]
    assert res == 'Data not defined'
    assert response.status_code == 400