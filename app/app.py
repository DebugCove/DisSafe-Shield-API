import secrets
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.initialize_functions import initialize_route, initialize_swagger
from app.middleware.compression import compression


csrf = CSRFProtect()


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(24)

    initialize_route(app)
    initialize_swagger(app)
    compression(app)
    csrf.init_app(app)

    @app.after_request
    def aplicar_cors(resposta):
        resposta.headers["Access-Control-Allow-Origin"] = "https://discord.com"
        resposta.headers["Access-Control-Allow-Methods"] = "GET, POST"
        resposta.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return resposta

    return app
