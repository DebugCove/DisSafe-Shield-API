from flask_compress import Compress

def compression(app):
    compression = Compress()
    compression.init_app(app)
