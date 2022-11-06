from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from src.lib.model import User


auth_user = HTTPBasicAuth()

@auth_user.verify_password
def verify_password_user(email, password):
    user_result = User.query.filter_by(email=email).first()

    if user_result and \
            check_password_hash(generate_password_hash(user_result.password), password):
        return email