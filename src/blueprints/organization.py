from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import Organization, SuperAdmin, db
from src.auth.auth_super_admin import auth


organization = Blueprint("organization", __name__, url_prefix="/api/v1/organization")

@organization.route("/", methods=["POST", "GET"])
@auth.login_required
def post_and_get_organization():

    super_admin_result = SuperAdmin.query.filter_by(email=auth.current_user()).first()

    if request.method == "GET":
        
        org_result = Organization.query.filter_by(super_admin_id=super_admin_result.id).all()

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
        # finally:
        #     db.session.close() # close session in this route will trigger error
        
        return jsonify({
            "name": body_data.get("name"),
            "description": body_data.get("description"),
            "super_admin_id": super_admin_result.id
        }), HTTP_201_CREATED

@organization.get("/<int:id>")
@auth.login_required
def get_organization(id):
    super_admin_result = SuperAdmin.query.filter_by(email=auth.current_user()).first()
    org_result = Organization.query.filter_by(id=id,super_admin_id=super_admin_result.id).first()

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
@auth.login_required
def delete_organization(id):
    super_admin_result = SuperAdmin.query.filter_by(email=auth.current_user()).first()
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
@organization.patch("/<int:id>")
@auth.login_required
def edit_organization(id):
    super_admin_result = SuperAdmin.query.filter_by(email=auth.current_user()).first()
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