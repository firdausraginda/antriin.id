from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import SuperAdmin, db


super_admin = Blueprint("super_admin", __name__, url_prefix="/api/v1/super_admin")

@super_admin.route("/", defaults={"id": None}, methods=["POST", "GET"])
@super_admin.route("/<int:id>", methods=["POST", "GET"])
def post_and_get_super_admin(id):

    if request.method == "GET":

        filters = ()
        if id:
            filters = filters + ((SuperAdmin.id == id),)
        super_admin_result = SuperAdmin.query.filter(*filters).all()

        data = []
        for super_admin in super_admin_result:
            data.append({
                "id": super_admin.id,
                "name": super_admin.name,
                "email": super_admin.email,
                "password": super_admin.password,
                "created_at": super_admin.created_at
            })
        
        return jsonify({
            "data": data
        }), HTTP_200_OK
           
    else:
        body_data = request.get_json()

        super_admin = SuperAdmin(
            name = body_data.get("name"),
            email = body_data.get("email"),
            password = body_data.get("password")
        )

        try:
            db.session.add(super_admin)
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
        }), HTTP_201_CREATED

@super_admin.get("/<int:id>")
def get_super_admin(id):
    super_admin_result = SuperAdmin.query.filter_by(id=id).first()

    if not super_admin_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    return jsonify({
        "id": super_admin_result.id,
        "name": super_admin_result.name,
        "email": super_admin_result.email,
        "password": super_admin_result.password,
        "created_at": super_admin_result.created_at
    }), HTTP_200_OK
            
@super_admin.delete("/<int:id>")
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
@super_admin.patch("/<int:id>")
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