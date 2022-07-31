from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import Organization, SuperAdmin, db
from src.auth.auth_super_admin import auth_super_admin
from flasgger import swag_from


organization = Blueprint("organization", __name__, url_prefix="/api/v1/organization")

@organization.route("/", defaults={"id": None}, methods=["POST", "GET"], endpoint="without_id")
@organization.route("/<int:id>", methods=["POST", "GET"], endpoint="with_id")
@auth_super_admin.login_required
@swag_from("../docs/organization/get_organization_using_auth_super_admin.yaml", endpoint="organization.without_id", methods=["GET"])
@swag_from("../docs/organization/get_organization_by_id_using_auth_super_admin.yaml", endpoint="organization.with_id", methods=["GET"])
@swag_from("../docs/organization/post_organization_user_using_auth_super_admin.yaml", endpoint="organization.without_id", methods=["POST"])
def post_and_get_organization(id):

    super_admin_result = SuperAdmin.query.filter_by(email=auth_super_admin.current_user()).first()

    if request.method == "GET":
        
        filters = (Organization.super_admin_id == super_admin_result.id,)
        if id:
            filters = filters + ((Organization.id == id),)
        org_result = Organization.query.filter(*filters).all()

        if not org_result:
            return jsonify({
                "message": "item not found!"
            }), HTTP_404_NOT_FOUND

        data = []
        for org in org_result:
            data.append({
                "id": org.id,
                "name": org.name,
                "created_at": org.created_at,
                "description": org.description,
                "super_admin_id": org.super_admin_id
            })
        
        return jsonify({
            "data": data
        }), HTTP_200_OK
           
    else:
        body_data = request.get_json()

        org = Organization(
            name = body_data.get("name"),
            description = body_data.get("description"),
            super_admin_id = super_admin_result.id
        )

        try:
            db.session.add(org)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        
        return jsonify({
            "name": body_data.get("name"),
            "description": body_data.get("description"),
            "super_admin_id": super_admin_result.id
        }), HTTP_201_CREATED
            
@organization.delete("/<int:id>")
@auth_super_admin.login_required
@swag_from("../docs/organization/delete_organization_by_id_using_auth_super_admin.yaml")
def delete_organization(id):
    super_admin_result = SuperAdmin.query.filter_by(email=auth_super_admin.current_user()).first()
    org_result = Organization.query.filter_by(id=id,super_admin_id=super_admin_result.id).first()

    if not org_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    try:
        db.session.delete(org_result)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return ({}), HTTP_204_NO_CONTENT

@organization.put("/<int:id>")
@auth_super_admin.login_required
@swag_from("../docs/organization/edit_organization_by_id_using_auth_super_admin.yaml")
def edit_organization(id):
    super_admin_result = SuperAdmin.query.filter_by(email=auth_super_admin.current_user()).first()
    org_result = Organization.query.filter_by(id=id,super_admin_id=super_admin_result.id).first()

    if not org_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    body_data = request.get_json()

    org_result.name = body_data.get("name")
    org_result.description = body_data.get("description")

    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return jsonify({
        "name": body_data.get("name"),
        "description": body_data.get("description"),
    }), HTTP_200_OK