from flask import Flask, jsonify
import os
from src.database import db
from src.endpoint_organization import organization
from src.endpoint_admin import admin
from src.endpoint_super_admin import super_admin


def create_app(test_config=None):
    
    app = Flask(__name__, 
        instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)

    @app.route("/")
    def root():
        return jsonify({
            "message": "hello world!"
        })

    db.app = app
    db.init_app(app)

    app.register_blueprint(organization)
    app.register_blueprint(admin)
    app.register_blueprint(super_admin)
    
    return app