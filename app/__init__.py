from flask import Flask
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    from . import recommender_app

    app.register_blueprint(recommender_app.bp)

    return app
