from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from sqlmodel import Session


def super_admin_auth(db_postgre_functionality: DBPostgreFunctionality):
    """authorize super admin using email & password"""

    auth_super_admin = HTTPBasicAuth()
    engine = db_postgre_functionality._engine

    @auth_super_admin.verify_password
    def verify_password_super_admin(email, password):

        with Session(engine) as session:
            super_admin_result = session.exec(
                db_postgre_functionality.get_super_admin_using_email(email)
            ).first()

        if super_admin_result and check_password_hash(
            generate_password_hash(super_admin_result.password), password
        ):
            return email

    return auth_super_admin
