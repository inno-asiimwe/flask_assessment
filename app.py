from flask import Flask, jsonify
from config import app_config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    from models.breeds import Breed
    from models.dogs import Dog
    db. init_app(app)

    from resources.breeds import breeds_api
    from resources.dogs import dogs_api
    from resources.statistics import stats_api

    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'message': 'Welcome to the dog api'}), 200

    app.register_blueprint(breeds_api, url_prefix='/api/v1/breeds')
    app.register_blueprint(dogs_api, url_prefix='/api/v1/dogs')
    app.register_blueprint(stats_api, url_prefix='/api/v1/statistics')

    return app
