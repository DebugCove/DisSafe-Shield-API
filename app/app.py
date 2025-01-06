import secrets
from flask import Flask
from flask_talisman import Talisman
from app.initialize_functions import initialize_route, initialize_swagger
from app.middleware.compression import compression


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(24)

    initialize_route(app)
    initialize_swagger(app)
    compression(app)
    Talisman(app)


    @app.after_request
    def security_settings(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers["Access-Control-Allow-Origin"] = "https://discord.com"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    return app
