from flask import Flask
from app.initialize_functions import initialize_route, initialize_swagger
from app.middleware.compression import compression


def create_app() -> Flask:
    app = Flask(__name__)

    initialize_route(app)
    initialize_swagger(app)
    compression(app)

    return app
