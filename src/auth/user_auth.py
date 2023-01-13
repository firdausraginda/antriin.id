from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from sqlmodel import Session


def user_auth(db_postgre_functionality: DBPostgreFunctionality):
    """authorize user using email & password"""

    auth_user = HTTPBasicAuth()
    engine = db_postgre_functionality._engine

    @auth_user.verify_password
    def verify_password_user(email, password):

        with Session(engine) as session:
            user_result = session.exec(
                db_postgre_functionality.get_user_using_user_email(email)
            ).first()

        if user_result and check_password_hash(
            generate_password_hash(user_result.password), password
        ):
            return email

    return auth_user
