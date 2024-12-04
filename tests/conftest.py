import pytest
import sys
import os
import logging
from flask import Flask
from flask.testing import FlaskClient, EnvironBuilder

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.app import create_app
from app.db.db import connect_database

@pytest.fixture(scope="session")
def configureLog():
    logging.basicConfig(level=logging.DEBUG)


@pytest.fixture()
def app(configureLog):

    logging.info("Test App Creation")

    flask_app = create_app()
    flask_app.config['TESTING'] = True

    yield flask_app


@pytest.fixture()
def client(app:Flask):
    with app.app_context():
        return app.test_client()


@pytest.fixture()
def runner(app:Flask):
    return app.test_cli_runner()


@pytest.fixture
def db(configureLog, client:FlaskClient):

    logging.info("Test DataBase Creation")

    with client.application.app_context():
        
        data_base = connect_database()
    
        data_base.autocommit = False

        assert data_base is not None

        yield data_base

        data_base.rollback()
        data_base.close()