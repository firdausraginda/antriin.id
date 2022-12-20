from flask import Blueprint, request, jsonify
from src.lib.custom_exception import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)
from src.lib.model import Admin, Organization, SuperAdmin, db
from src.auth.auth_super_admin import auth_super_admin
from flasgger import swag_from


def process_admin(admin_usecase):

    admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

    @admin.get("/", defaults={"admin_id": None})
    @admin.get("/<int:admin_id>")
    @auth_super_admin.login_required
    @swag_from("../docs/admin/get_admin_using_auth_super_admin.yaml")
    @swag_from("../docs/admin/get_admin_by_id_using_auth_super_admin.yaml")
    def get_admin(admin_id):

        result = admin_usecase.get_admin(auth_super_admin.current_user(), admin_id)

        return jsonify({"data": result["data"]}), result["status_code"]

    @admin.post("/")
    @auth_super_admin.login_required
    @swag_from("../docs/admin/post_admin_using_auth_super_admin.yaml")
    def post_admin():

        body_data = request.get_json()
        result = admin_usecase.post_admin(auth_super_admin.current_user(), body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    @admin.delete("/<int:admin_id>")
    @auth_super_admin.login_required
    @swag_from("../docs/admin/delete_admin_by_id_using_auth_super_admin.yaml")
    def delete_admin(admin_id):

        result = admin_usecase.delete_admin(auth_super_admin.current_user(), admin_id)

        return jsonify({"data": result["data"]}), result["status_code"]

    @admin.put("/<int:admin_id>")
    @auth_super_admin.login_required
    @swag_from("../docs/admin/edit_admin_by_id_using_auth_super_admin.yaml")
    def edit_admin(admin_id):

        body_data = request.get_json()
        result = admin_usecase.edit_admin(
            auth_super_admin.current_user(), admin_id, body_data
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    return admin
