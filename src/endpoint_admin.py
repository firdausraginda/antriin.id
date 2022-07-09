from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import Admin, db


admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

@admin.route("/", methods=["POST", "GET"])
def post_and_get_admin():

    if request.method == "GET":
        admin_result = Admin.query.all()

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
            name=body_data.get("name"),
            email=body_data.get("email"),
            password=body_data.get("password"),
            organization_id=body_data.get("organization_id")
        )

        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            "name":body_data.get("name"),
            "email":body_data.get("email"),
            "password":body_data.get("password"),
            "organization_id":body_data.get("organization_id")
        }), HTTP_201_CREATED