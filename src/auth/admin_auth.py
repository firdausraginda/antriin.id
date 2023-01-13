from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from sqlmodel import Session


def admin_auth(db_postgre_functionality: DBPostgreFunctionality):
    """authorize admin using email & password"""

    auth_admin = HTTPBasicAuth()
    engine = db_postgre_functionality._engine

    @auth_admin.verify_password
    def verify_password_admin(email, password):

        with Session(engine) as session:
            admin_result = session.exec(
                db_postgre_functionality.get_admin_using_admin_email(email)
            ).first()

        if admin_result and check_password_hash(
            generate_password_hash(admin_result.password), password
        ):
            return email

    return auth_admin
