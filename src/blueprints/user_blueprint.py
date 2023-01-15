from flask import Blueprint, request, jsonify
from flasgger import swag_from


def process_user(user_usecase, admin_auth, user_auth):

    user = Blueprint("user", __name__, url_prefix="/api/v1/user")

    @user.get("/", defaults={"user_id": None})
    @user.get("/<int:user_id>")
    @admin_auth.login_required
    @swag_from("../docs/user/get_user_using_auth_admin.yaml")
    @swag_from("../docs/user/get_user_by_id_using_auth_admin.yaml")
    def get_user_by_auth_admin(user_id):

        result = user_usecase.get_user_by_admin(admin_auth.current_user(), user_id)

        return jsonify({"data": result["data"]}), result["status_code"]

    @user.get("/profile")
    @user_auth.login_required
    @swag_from("../docs/user/get_user_using_auth_user.yaml")
    def get_user_by_auth_user():

        result = user_usecase.get_user_by_user(user_auth.current_user())

        return jsonify({"data": result["data"]}), result["status_code"]

    @user.post("/signup")
    @swag_from("../docs/user/post_user.yaml")
    def post_user():

        body_data = request.get_json()
        result = user_usecase.post_user(body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    @user.delete("/profile")
    @user_auth.login_required
    @swag_from("../docs/user/delete_user_using_auth_user.yaml")
    def delete_user_by_user():

        result = user_usecase.delete_user_by_user(user_auth.current_user())

        return jsonify({"data": result["data"]}), result["status_code"]

    @user.put("/profile")
    @user_auth.login_required
    @swag_from("../docs/user/edit_user_using_auth_user.yaml")
    def edit_admin():

        body_data = request.get_json()
        result = user_usecase.edit_user_by_user(user_auth.current_user(), body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    return user
