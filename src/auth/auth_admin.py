from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import Admin


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password_admin(email, password):
    admin_result = Admin.query.filter_by(email=email).first()

    if admin_result and \
            check_password_hash(generate_password_hash(admin_result.password), password):
        return email