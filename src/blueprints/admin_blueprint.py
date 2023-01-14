from flask import Blueprint, request, jsonify
from flasgger import swag_from


def process_admin(admin_usecase, auth_admin):

    admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

    @admin.get("/")
    @auth_admin.login_required
    @swag_from("../docs/admin/get_admin_using_auth_admin.yaml")
    def get_admin():

        result = admin_usecase.get_admin(auth_admin.current_user())

        return jsonify({"data": result["data"]}), result["status_code"]

    @admin.post("/")
    @swag_from("../docs/admin/post_admin.yaml")
    def post_admin():

        body_data = request.get_json()
        result = admin_usecase.post_admin(body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    @admin.delete("/")
    @auth_admin.login_required
    @swag_from("../docs/admin/delete_admin_using_auth_admin.yaml")
    def delete_admin():

        result = admin_usecase.delete_admin(auth_admin.current_user())

        return jsonify({"data": result["data"]}), result["status_code"]

    @admin.put("/")
    @auth_admin.login_required
    @swag_from("../docs/admin/edit_admin_using_auth_admin.yaml")
    def edit_admin():

        body_data = request.get_json()
        result = admin_usecase.edit_admin(auth_admin.current_user(), body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    return admin
