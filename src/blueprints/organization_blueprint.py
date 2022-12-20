from flask import Blueprint, request, jsonify
from src.auth.auth_super_admin import auth_super_admin
from flasgger import swag_from


def process_organization(organization_usecase):

    organization = Blueprint(
        "organization", __name__, url_prefix="/api/v1/organization"
    )

    @organization.get("/")
    @auth_super_admin.login_required
    @swag_from("../docs/organization/get_organization_using_auth_super_admin.yaml")
    def get_organization():

        result = organization_usecase.get_organization(auth_super_admin.current_user())

        return jsonify({"data": result["data"]}), result["status_code"]

    @organization.post("/")
    @auth_super_admin.login_required
    @swag_from(
        "../docs/organization/post_organization_user_using_auth_super_admin.yaml"
    )
    def post_organization():

        body_data = request.get_json()
        result = organization_usecase.post_organization(
            auth_super_admin.current_user(), body_data
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    @organization.delete("/")
    @auth_super_admin.login_required
    @swag_from(
        "../docs/organization/delete_organization_by_id_using_auth_super_admin.yaml"
    )
    def delete_organization():

        result = organization_usecase.delete_organization(
            auth_super_admin.current_user()
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    @organization.put("/")
    @auth_super_admin.login_required
    @swag_from(
        "../docs/organization/edit_organization_by_id_using_auth_super_admin.yaml"
    )
    def edit_organization():

        body_data = request.get_json()
        result = organization_usecase.edit_organization(
            auth_super_admin.current_user(), body_data
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    return organization
