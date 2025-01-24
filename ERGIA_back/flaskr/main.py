from datetime import timedelta
import os

from flasgger import Swagger
from flask import Flask, request
from flask_cors import CORS

import logging

from flaskr.controllers.authentication_controller import login_bp
from flaskr.controllers.scu_controller import scu_bp
from flaskr.controllers.campaign_controller import campaigns_bp, create_campaign
from flaskr.controllers.register_controller import register_bp
from flaskr.controllers.corpus_controller import corpus_bp
from flaskr.controllers.annotation_controller import annotation_bp

    
from flask_jwt_extended import JWTManager
from flaskr.app_logging.error_handler import register_error_handler
from flaskr.app_logging.logs_gestion import register_before_request, register_after_request

request_logger = logging.getLogger('request_logger')
request_logger.setLevel(logging.INFO)
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)

if os.path.isdir("logs")!=True:
    os.mkdir("logs")

request_handler = logging.FileHandler('logs/requests_log.json')
error_handler = logging.FileHandler('logs/errors_log.json')

formatter = logging.Formatter('%(message)s')
request_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

request_logger.addHandler(request_handler)
error_logger.addHandler(error_handler)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    template = {
        "swagger": "2.0",
        "info": {
            "title": "FLASK ERGIA API",
            "description": "API développée en Python Flask, fournissant une interface entre la base de données et le proxy dédiés à l'application."
        },
        "tags": [
            {
                "name": "Authentification",
                "description": "Endpoints liés à l'authentification"
            },
            {
                "name": "Campagnes",
                "description": "Endpoints liés à la gestion des campagnes"
            },
            {
                "name": "Corpus",
                "description": "Endpoints liés à la gestion des corpus"
            },
            {
                "name": "SCU",
                "description": "Endpoints liés à la gestion des SCU"
            }
        ]
    }
    app.config['SWAGGER'] = {
        'title': 'FLASK ERGIA API',
        'uiversion': 2,
        'template': './resources/flasgger/swagger_ui.html'
    }

    Swagger(app, template=template)
    app.config['LOGIN_KEY'] = 'http://127.0.0.1:5000'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

    jwt = JWTManager(app)
    CORS(app)
    register_before_request(app)
    register_after_request(app, request_logger)
    register_error_handler(app, error_logger)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    app.register_blueprint(login_bp)
    app.register_blueprint(scu_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(corpus_bp)
    app.register_blueprint(annotation_bp)
    
    return app