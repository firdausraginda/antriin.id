from flask import Blueprint, request, jsonify
from src.auth.auth_admin import auth_admin
from src.auth.auth_user import auth_user
from flasgger import swag_from


def process_user(user_usecase):

    user = Blueprint("user", __name__, url_prefix="/api/v1/user")

    @user.get("/", defaults={"user_id": None})
    @user.get("/<int:user_id>")
    @auth_admin.login_required
    @swag_from("../docs/user/get_user_using_auth_admin.yaml")
    @swag_from("../docs/user/get_user_by_id_using_auth_admin.yaml")
    def get_user_by_auth_admin(user_id):

        result = user_usecase.get_user_by_admin(auth_admin.current_user(), user_id)

        return jsonify({"data": result["data"]}), result["status_code"]

    @user.get("/profile")
    @auth_user.login_required
    @swag_from("../docs/user/get_user_using_auth_user.yaml")
    def get_user_by_auth_user():

        result = user_usecase.get_user_by_user(auth_user.current_user())

        return jsonify({"data": result["data"]}), result["status_code"]

    @user.post("/signup")
    @swag_from("../docs/user/post_user.yaml")
    def post_user():

        body_data = request.get_json()
        result = user_usecase.post_user(body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    @user.delete("/profile")
    @auth_user.login_required
    @swag_from("../docs/user/delete_user_using_auth_user.yaml")
    def delete_user_by_user():

        result = user_usecase.delete_user_by_user(auth_user.current_user())

        return jsonify({"data": result["data"]}), result["status_code"]

    @user.put("/profile")
    @auth_user.login_required
    @swag_from("../docs/user/edit_user_using_auth_user.yaml")
    def edit_admin():

        body_data = request.get_json()
        result = user_usecase.edit_user_by_user(auth_user.current_user(), body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    return user
