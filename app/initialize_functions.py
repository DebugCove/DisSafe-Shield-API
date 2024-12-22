from flask import Flask
from flasgger import Swagger
from app.modules.main.route import main_report, main


def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(main, url_prefix='/api/v1')
        app.register_blueprint(main_report, url_prefix='/api/v1/report')

def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger
