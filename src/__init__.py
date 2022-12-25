from flask import Flask, jsonify
import os

# import swagger
from flasgger import Swagger
from src.docs.swagger import template, swagger_config

# import blueprint
from src.blueprints.super_admin_blueprint import process_super_admin
from src.blueprints.organization_blueprint import process_organization
from src.blueprints.admin_blueprint import process_admin
from src.blueprints.queue_blueprint import process_queue
from src.blueprints.queue_user_blueprint import process_queue_user
from src.blueprints.user_blueprint import process_user

# import usecase
from src.usecase.super_admin_usecase import SuperAdminUsecase
from src.usecase.organization_usecase import OrganizationUsecase
from src.usecase.admin_usecase import AdminUsecase
from src.usecase.queue_usecase import QueueUsecase
from src.usecase.queue_user_usecase import QueueUserUsecase
from src.usecase.user_usecase import UserUsecase

# import functionality
from src.functionality.db_postgre_functionality import DBPostgreFunctionality

# import lib
from src.lib.model import db


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SWAGGER={"title": "antriin.id API", "uiversion": 3},
        )
    else:
        app.config.from_mapping(test_config)

    @app.get("/health")
    def check_health():
        return jsonify({"message": "running well!"})

    # init functionality
    db_postgre_functionality = DBPostgreFunctionality()

    # init usecase
    super_admin_usecase = SuperAdminUsecase(db_postgre_functionality)
    organization_usecase = OrganizationUsecase(db_postgre_functionality)
    admin_usecase = AdminUsecase(db_postgre_functionality)
    queue_usecase = QueueUsecase(db_postgre_functionality)
    queue_user_usecase = QueueUserUsecase(db_postgre_functionality)
    user_usecase = UserUsecase(db_postgre_functionality)

    # init app
    db.app = app
    db.init_app(app)

    # init blueprint
    app.register_blueprint(process_super_admin(super_admin_usecase))
    app.register_blueprint(process_organization(organization_usecase))
    app.register_blueprint(process_admin(admin_usecase))
    app.register_blueprint(process_queue(queue_usecase))
    app.register_blueprint(process_queue_user(queue_user_usecase))
    app.register_blueprint(process_user(user_usecase))

    Swagger(app, config=swagger_config, template=template)

    return app
