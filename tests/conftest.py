import pytest
import sys
import os
import logging
from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.app import create_app
from app.db.db import connect_database


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