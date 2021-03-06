from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from src.database import Admin, Organization, SuperAdmin, db
from src.auth.auth_super_admin import auth_super_admin


admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

@admin.route("/", defaults={"id": None}, methods=["POST", "GET"])
@admin.route("/<int:id>", methods=["POST", "GET"])
@auth_super_admin.login_required
def post_and_get_admin(id):

    super_admin_result = SuperAdmin.query.filter_by(email=auth_super_admin.current_user()).first()
    organization_result = Organization.query.filter_by(super_admin_id=super_admin_result.id).first()

    if not super_admin_result or not organization_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    if request.method == "GET":

        filters = (Admin.organization_id == organization_result.id,)
        if id:
            filters = filters + ((Admin.id == id),)
        admin_result = Admin.query.filter(*filters).all()

        if not admin_result:
            return jsonify({
                "message": "item not found!"
            }), HTTP_404_NOT_FOUND

        data = []
        for admin in admin_result:
            data.append({
                "id": admin.id,
                "name": admin.name,
                "email": admin.email,
                "password": admin.password,
                "created_at": admin.created_at,
                "organization_id": admin.organization_id
            })
        
        return jsonify({
            "data": data
        }), HTTP_200_OK
           
    else:
        body_data = request.get_json()

        admin = Admin(
            name = body_data.get("name"),
            email = body_data.get("email"),
            password = body_data.get("password"),
            organization_id = organization_result.id
        )

        try:
            db.session.add(admin)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        
        return jsonify({
            "name": body_data.get("name"),
            "email": body_data.get("email"),
            "password": body_data.get("password"),
            "organization_id": organization_result.id
        }), HTTP_201_CREATED

@admin.get("/<int:id>")
@auth_super_admin.login_required
def get_admin(id):
    super_admin_result = SuperAdmin.query.filter_by(email=auth_super_admin.current_user()).first()
    organization_result = Organization.query.filter_by(super_admin_id=super_admin_result.id).first()
    admin_result = Admin.query.filter_by(id=id,organization_id=organization_result.id).first()

    if not admin_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    return jsonify({
        "id": admin_result.id,
        "name": admin_result.name,
        "email": admin_result.email,
        "password": admin_result.password,
        "created_at": admin_result.created_at
    }), HTTP_200_OK
            
@admin.delete("/<int:id>")
@auth_super_admin.login_required
def delete_admin(id):
    super_admin_result = SuperAdmin.query.filter_by(email=auth_super_admin.current_user()).first()
    organization_result = Organization.query.filter_by(super_admin_id=super_admin_result.id).first()
    admin_result = Admin.query.filter_by(id=id,organization_id=organization_result.id).first()

    if not admin_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    try:
        db.session.delete(admin_result)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return ({}), HTTP_204_NO_CONTENT

@admin.put("/<int:id>")
@admin.patch("/<int:id>")
@auth_super_admin.login_required
def edit_admin(id):
    super_admin_result = SuperAdmin.query.filter_by(email=auth_super_admin.current_user()).first()
    organization_result = Organization.query.filter_by(super_admin_id=super_admin_result.id).first()
    admin_result = Admin.query.filter_by(id=id,organization_id=organization_result.id).first()

    if not admin_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    body_data = request.get_json()
    admin_result.name = body_data.get("name")
    admin_result.email = body_data.get("email")
    admin_result.password = body_data.get("password")

    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return jsonify({
        "name": body_data.get("name"),
        "email": body_data.get("email"),
        "password": body_data.get("password")
    }), HTTP_200_OK