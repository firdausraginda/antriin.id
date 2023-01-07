from flask import Blueprint, request, jsonify
from flasgger import swag_from


def process_admin(admin_usecase, auth_super_admin):

    admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

    @admin.get("/", defaults={"admin_id": None}, endpoint="without_id")
    @admin.get("/<int:admin_id>", endpoint="with_id")
    @auth_super_admin.login_required
    @swag_from(
        "../docs/admin/get_admin_using_auth_super_admin.yaml",
        endpoint="admin.without_id",
    )
    @swag_from(
        "../docs/admin/get_admin_by_id_using_auth_super_admin.yaml",
        endpoint="admin.with_id",
    )
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
