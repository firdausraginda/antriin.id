from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import Organization, db

organizations = Blueprint("organizations", __name__, url_prefix="/api/v1/organizations")

@organizations.route("/", methods=["POST", "GET"])
def post_and_get_organizations():

    if request.method == "GET":
        org_result = Organization.query.all()

        data = []
        for org in org_result:
            data.append({
                "id": org.id,
                "name": org.name,
                "created_at": org.created_at,
                "description": org.description
            })
        
        return jsonify({
            "data": data
        }), HTTP_200_OK
           
    else:
        body_data = request.get_json()

        org = Organization(
            id=body_data.get("id"),
            name=body_data.get("name"),
            created_at=body_data.get("created_at"),
            description=body_data.get("description")
        )

        db.session.add(org)
        db.session.commit()
        
        return jsonify({
            "name": body_data.get("name"),
            "description": body_data.get("description")
        }), HTTP_201_CREATED

@organizations.get("/<int:id>")
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
        "description": org_result.description
    }), HTTP_200_OK
            
@organizations.delete("/<int:id>")
def delete_organization(id):
    org_result = Organization.query.filter_by(id=id).first()

    if not org_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    db.session.delete(org_result)
    db.session.commit()

    return ({}), HTTP_204_NO_CONTENT

@organizations.put("/<int:id>")
@organizations.patch("/<int:id>")
def edit_organization(id):
    org_result = Organization.query.filter_by(id=id).first()

    if not org_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    body_data = request.get_json()

    org_result.name = body_data.get("name")
    org_result.description = body_data.get("description")

    db.session.commit()

    return jsonify({
        "name": body_data.get("name"),
        "description": body_data.get("description")
    }), HTTP_200_OK