from flask import Blueprint, request, jsonify
from flasgger import swag_from


def process_organization(organization_usecase, admin_auth):

    organization = Blueprint(
        "organization", __name__, url_prefix="/api/v1/organization"
    )

    @organization.get("/")
    @admin_auth.login_required
    @swag_from("../docs/organization/get_organization_using_auth_admin.yaml")
    def get_organization():

        result = organization_usecase.get_organization(admin_auth.current_user())

        return jsonify({"data": result["data"]}), result["status_code"]

    @organization.post("/")
    @admin_auth.login_required
    @swag_from("../docs/organization/post_organization_user_using_auth_admin.yaml")
    def post_organization():

        body_data = request.get_json()
        result = organization_usecase.post_organization(
            admin_auth.current_user(), body_data
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    @organization.delete("/")
    @admin_auth.login_required
    @swag_from("../docs/organization/delete_organization_using_auth_admin.yaml")
    def delete_organization():

        result = organization_usecase.delete_organization(admin_auth.current_user())

        return jsonify({"data": result["data"]}), result["status_code"]

    @organization.put("/")
    @admin_auth.login_required
    @swag_from("../docs/organization/edit_organization_using_auth_admin.yaml")
    def edit_organization():

        body_data = request.get_json()
        result = organization_usecase.edit_organization(
            admin_auth.current_user(), body_data
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    return organization
