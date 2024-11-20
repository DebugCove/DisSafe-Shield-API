from flask import Flask
from flasgger import Swagger
from app.modules.main.route import main_bp


def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(main_bp, url_prefix='/api/v1')

def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger
