from os import getenv
from dotenv import load_dotenv
from app.app import create_app

load_dotenv()
config = getenv('FLASK_ENV') or 'development'

app = create_app(config)

if __name__ == "__main__":
    HOST = getenv('HOST')
    if config == 'development':
        DEBUG = getenv('DEBUG_DEVELOPMENT')
        PORT = getenv('PORT_DEVELOPMENT')
    else:
        DEBUG = getenv('DEBUG_PRODUCTION')
        PORT = getenv('PORT_PRODUCTION')

    app.run(debug=DEBUG, host=HOST, port=PORT)
