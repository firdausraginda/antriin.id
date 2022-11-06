from flask import Blueprint, request, jsonify
from src.lib.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.lib.model import SuperAdmin, db
from flasgger import swag_from


def process_super_admin(super_admin_usecase):

    super_admin = Blueprint("super_admin", __name__, url_prefix="/api/v1/super_admin")

    @super_admin.route("/", defaults={"super_admin_id": None}, methods=["POST", "GET"], endpoint="without_id")
    @super_admin.route("/<int:super_admin_id>", methods=["GET"], endpoint="with_id")
    @swag_from("../docs/super_admin/get_super_admin_by_id.yaml", endpoint="super_admin.with_id", methods=["GET"])
    @swag_from("../docs/super_admin/post_super_admin.yaml", endpoint="super_admin.without_id", methods=["POST"])
    def post_and_get_super_admin(super_admin_id):

        if request.method == "GET":
            
            result = super_admin_usecase.get_super_admin(super_admin_id)

            return jsonify({
                "data": result["data"]
            }), result["message"]
        else:
            body_data = request.get_json()

            result = super_admin_usecase.post_super_admin(body_data)

            return jsonify({
                "data": result["data"]
            }), result["message"]
                
    @super_admin.delete("/<int:id>")
    @swag_from("../docs/super_admin/delete_super_admin_by_id.yaml")
    def delete_super_admin(id):
        super_admin_result = SuperAdmin.query.filter_by(id=id).first()

        if not super_admin_result:
            return jsonify({
                "message": "item not found!"
            }), HTTP_404_NOT_FOUND
        
        try:
            db.session.delete(super_admin_result)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

        return ({}), HTTP_204_NO_CONTENT

    @super_admin.put("/<int:id>")
    @swag_from("../docs/super_admin/edit_super_admin_by_id.yaml")
    def edit_super_admin(id):
        super_admin_result = SuperAdmin.query.filter_by(id=id).first()

        if not super_admin_result:
            return jsonify({
                "message": "item not found!"
            }), HTTP_404_NOT_FOUND
        
        body_data = request.get_json()

        super_admin_result.name = body_data.get("name")
        super_admin_result.email = body_data.get("email")
        super_admin_result.password = body_data.get("password")

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

    return super_admin