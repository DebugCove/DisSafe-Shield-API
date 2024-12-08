import pytest
import sys
import os
import logging
from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.app import create_app
from app.db.db import connect_database




@pytest.fixture(scope="session")
def configureLog():
    logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="session")
def app(configureLog):

    logging.info("Test App Creation")

    flask_app = create_app()
    flask_app.config['TESTING'] = True

    yield flask_app


@pytest.fixture(scope="session")
def client(app:Flask):
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app:Flask):
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def db(configureLog, app:Flask):
        
    data_base = connect_database()

    assert data_base is not None

    @app.after_request
    def rollback_db(response):
        if data_base.is_connected:
            data_base.rollback()
        return response

    yield data_base

    data_base.rollback()
    data_base.close()