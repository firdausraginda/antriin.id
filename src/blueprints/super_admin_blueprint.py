from flask import Blueprint, request, jsonify
from flasgger import swag_from


def process_super_admin(super_admin_usecase):

    super_admin = Blueprint("super_admin", __name__, url_prefix="/api/v1/super_admin")

    @super_admin.get("/<int:super_admin_id>")
    @swag_from("../docs/super_admin/get_super_admin_by_id.yaml")
    def get_super_admin(super_admin_id):

        result = super_admin_usecase.get_super_admin(super_admin_id)

        return jsonify({"data": result["data"]}), result["status_code"]

    @super_admin.post("/")
    @swag_from("../docs/super_admin/post_super_admin.yaml")
    def post_super_admin():

        body_data = request.get_json()
        result = super_admin_usecase.post_super_admin(body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    @super_admin.delete("/<int:super_admin_id>")
    @swag_from("../docs/super_admin/delete_super_admin_by_id.yaml")
    def delete_super_admin(super_admin_id):

        result = super_admin_usecase.delete_super_admin(super_admin_id)

        return jsonify({"data": result["data"]}), result["status_code"]

    @super_admin.put("/<int:super_admin_id>")
    @swag_from("../docs/super_admin/edit_super_admin_by_id.yaml")
    def edit_super_admin(super_admin_id):

        body_data = request.get_json()
        result = super_admin_usecase.edit_super_admin(super_admin_id, body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    return super_admin
