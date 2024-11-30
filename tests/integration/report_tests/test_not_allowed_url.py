import logging
from flask.testing import FlaskClient

def test(client:FlaskClient, url_prefix, succesReportData, createTokenRow):

    url = "http://youtube.com"
    succesReportData["proof"] = url

    if createTokenRow:

        response = client.post(f"{url_prefix}/report",
                                    
            json = succesReportData,
            headers = {
                "Authorization": f"Bearer {createTokenRow}"
            }
        )
        json = response.get_json()
        res = json["message"]
        assert res == 'Report was completed successfully, but some links were not included.'
        assert response.status_code == 400

    else:
        logging.error("Test Failed. Reason: hasn't token.")