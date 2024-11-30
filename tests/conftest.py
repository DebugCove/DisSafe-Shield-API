import pytest
import sys
import os
import logging
from flask import Flask
from flask.testing import FlaskClient, EnvironBuilder

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.app import create_app
from app.db.db import connect_database

#def doResquest(client:FlaskClient, method:str, url:str, json:dict, data:dict):



@pytest.fixture
def configureLog():
    logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def app(configureLog):

    logging.info("Test App Creation")

    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
    })

    yield flask_app


@pytest.fixture
def client(app:Flask):
    return app.test_client()


@pytest.fixture
def runner(app:Flask):
    return app.test_cli_runner()


@pytest.fixture
def db(configureLog):

    logging.info("Test DataBase Creation")

    data_base = connect_database()
    data_base.autocommit = False

    yield data_base

    data_base.rollback()
    data_base.close()