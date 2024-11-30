import logging
from flask.testing import FlaskClient

def test(client:FlaskClient, url_prefix, succesReportData, createTokenRow):
    logging.info("Succes report route test started")

    if createTokenRow:
        response = client.post(f"{url_prefix}/report",
                                    
            json = succesReportData,
            headers = {
                "Authorization": f"Bearer {createTokenRow}"
            }
        )
        json = response.get_json()
        assert json
        res = json["message"]
        assert res == 'Report sent successfully.'
        assert response.status_code == 200
    else:
        logging.error("Test Failed. Reason: hasn't token.")