from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import SuperAdmin


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password_super_admin(email, password):
    super_admin_result = SuperAdmin.query.filter_by(email=email).first()

    if super_admin_result and \
            check_password_hash(generate_password_hash(super_admin_result.password), password):
        return email