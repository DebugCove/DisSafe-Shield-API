from flask import Flask
from app.initialize_functions import initialize_route, initialize_swagger

def create_app(config=None) -> Flask:
    app = Flask(__name__)

    initialize_route(app)
    initialize_swagger(app)

    return app
