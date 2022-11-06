from flask import Flask, jsonify
import os
from src.lib.model import db
from src.blueprints.organization import organization
from src.blueprints.admin import admin
from src.blueprints.queue import queue
from src.blueprints.queue_user import queue_user
from src.blueprints.user import user
from flasgger import Swagger
from src.docs.swagger import template, swagger_config

from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from src.usecase.super_admin_usecase import SuperAdminUsecase
from src.blueprints.super_admin import process_super_admin

def create_app(test_config=None):
    
    app = Flask(__name__, 
        instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SWAGGER = {
                "title": "antriin.id API",
                "uiversion": 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    @app.get("/health")
    def check_health():
        return jsonify({
            "message": "running well!"
        })
    
    # init repo
    db_postgre_functionality = DBPostgreFunctionality()

    # init usecase
    super_admin_usecase = SuperAdminUsecase(db_postgre_functionality)

    db.app = app
    db.init_app(app)

    app.register_blueprint(organization)
    app.register_blueprint(admin)
    app.register_blueprint(process_super_admin(super_admin_usecase))
    # app.register_blueprint(super_admin)
    app.register_blueprint(queue)
    app.register_blueprint(queue_user)
    app.register_blueprint(user)

    Swagger(app, config=swagger_config, template=template)
    
    return app