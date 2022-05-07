from flask import Flask


def create_app():
    app = Flask(__name__)

    from . import recommender_app

    app.register_blueprint(recommender_app.bp)

    return app
