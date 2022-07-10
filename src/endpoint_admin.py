from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED
from src.database import Admin, Organization, SuperAdmin, db
from src.auth.auth_super_admin import auth


admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

@admin.route("/", methods=["POST", "GET"])
@auth.login_required
def post_and_get_admin():

    super_admin_result = SuperAdmin.query.filter_by(email=auth.current_user()).first()
    organization_result = Organization.query.filter_by(super_admin_id=super_admin_result.id).first()

    if request.method == "GET":
        admin_result = Admin.query.filter_by(organization_id=organization_result.id).all()

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

        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            "name": body_data.get("name"),
            "email": body_data.get("email"),
            "password": body_data.get("password"),
            "organization_id": organization_result.id
        }), HTTP_201_CREATED