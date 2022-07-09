from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import Organization, db


organization = Blueprint("organization", __name__, url_prefix="/api/v1/organization")

@organization.route("/", methods=["POST", "GET"])
def post_and_get_organization():

    if request.method == "GET":
        org_result = Organization.query.all()

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
            name=body_data.get("name"),
            description=body_data.get("description"),
            super_admin_id=body_data.get("super_admin_id")
        )

        db.session.add(org)
        db.session.commit()
        
        return jsonify({
            "name": body_data.get("name"),
            "description": body_data.get("description"),
            "super_admin_id": body_data.get("super_admin_id")
        }), HTTP_201_CREATED

@organization.get("/<int:id>")
def get_organization(id):
    org_result = Organization.query.filter_by(id=id).first()

    if not org_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    return jsonify({
        "id": org_result.id,
        "name": org_result.name,
        "created_at": org_result.created_at,
        "description": org_result.description,
        "super_admin_id": org_result.super_admin_id
    }), HTTP_200_OK
            
@organization.delete("/<int:id>")
def delete_organization(id):
    org_result = Organization.query.filter_by(id=id).first()

    if not org_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    db.session.delete(org_result)
    db.session.commit()

    return ({}), HTTP_204_NO_CONTENT

@organization.put("/<int:id>")
@organization.patch("/<int:id>")
def edit_organization(id):
    org_result = Organization.query.filter_by(id=id).first()

    if not org_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    body_data = request.get_json()

    org_result.name = body_data.get("name")
    org_result.description = body_data.get("description")
    org_result.super_admin_id = body_data.get("super_admin_id")

    db.session.commit()

    return jsonify({
        "name": body_data.get("name"),
        "description": body_data.get("description"),
        "super_admin_id": body_data.get("super_admin_id")
    }), HTTP_200_OK