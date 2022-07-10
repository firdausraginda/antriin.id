from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from src.constants.http_status_code import HTTP_404_NOT_FOUND
from werkzeug.security import check_password_hash
from src.database import SuperAdmin


# auth = HTTPBasicAuth()

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and \
#             check_password_hash(users.get(username), password):
#         return username

# @auth.verify_password
# def verify_password_super_admin(email, password):
#     super_admin_result = SuperAdmin.query.filter_by(email=email).first()

#     if not super_admin_result:
#         return jsonify({
#             "message": "item not found!"
#         }), HTTP_404_NOT_FOUND

#     if super_admin_result and \
#             check_password_hash(super_admin_result.password, password):
#         return email

# @app.route('/')
# @auth.login_required
# def index():
#     return jsonify({
#         "current user": auth.current_user(),
#         "users": users[auth.current_user()]
#     })