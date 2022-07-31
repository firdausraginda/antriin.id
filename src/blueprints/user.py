from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from src.database import Admin, User, Queue, QueueUser, db
from src.auth.auth_admin import auth_admin
from src.auth.auth_user import auth_user
from flasgger import swag_from


user = Blueprint("user", __name__, url_prefix="/api/v1/user")

@user.route("/", defaults={"id": None}, methods=["POST", "GET"], endpoint="without_id")
@user.route("/<int:id>", methods=["POST", "GET"], endpoint="with_id")
@auth_admin.login_required
@swag_from("../docs/user/get_user_using_auth_admin.yaml", endpoint="user.without_id", methods=["GET"])
@swag_from("../docs/user/get_user_by_id_using_auth_admin.yaml", endpoint="user.with_id", methods=["GET"])
@swag_from("../docs/user/post_user_using_auth_admin.yaml", endpoint="user.without_id", methods=["POST"])
def post_and_get_user_by_auth_admin(id):

    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()

    if request.method == "GET":

        queue_result = Queue.query.filter_by(admin_id=admin_result.id).all()
        queue_user_result = QueueUser.query.filter(QueueUser.queue_id.in_([queue.id for queue in queue_result])).all()
        filters = (User.id.in_([queue_user.user_id for queue_user in queue_user_result]),)
        if id:
            filters = filters + ((User.id == id),)
        user_result = User.query.filter(*filters).all()

        if not user_result or not queue_user_result:
            return jsonify({
                "message": "item not found!"
            }), HTTP_404_NOT_FOUND

        data = []
        for user in user_result:
            data.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "created_at": user.created_at
            })
        
        return jsonify({
            "data": data
        }), HTTP_200_OK
           
    else:
        body_data = request.get_json()

        user = User(
            name = body_data.get("name"),
            email = body_data.get("email"),
            password = body_data.get("password")
        )

        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        
        return jsonify({
            "name": body_data.get("name"),
            "email": body_data.get("email"),
            "password": body_data.get("password")
        }), HTTP_201_CREATED

@user.get("/profile")
@auth_user.login_required
@swag_from("../docs/user/get_user_by_id_using_auth_user.yaml")
def get_user_by_auth_user():

    user_result = User.query.filter_by(email=auth_user.current_user()).first()

    return jsonify({
        "id": user_result.id,
        "name": user_result.name,
        "email": user_result.email,
        "password": user_result.password,
        "created_at": user_result.created_at
    }), HTTP_200_OK

@user.post("/signup")
@swag_from("../docs/user/post_user.yaml")
def post_user():

    body_data = request.get_json()

    user = User(
        name = body_data.get("name"),
        email = body_data.get("email"),
        password = body_data.get("password")
    )

    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    
    return jsonify({
        "name": body_data.get("name"),
        "email": body_data.get("email"),
            "password": body_data.get("password")
        }), HTTP_201_CREATED


@user.delete("/profile")
@auth_user.login_required
@swag_from("../docs/user/delete_user_using_auth_user.yaml")
def delete_admin():
    
    user_result = User.query.filter_by(email=auth_admin.current_user()).first()

    if not user_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    try:
        db.session.delete(user_result)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return ({}), HTTP_204_NO_CONTENT

@user.put("/profile")
@auth_user.login_required
@swag_from("../docs/user/edit_user_using_auth_user.yaml")
def edit_admin():
    
    user_result = User.query.filter_by(email=auth_user.current_user()).first()

    if not user_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    body_data = request.get_json()
    user_result.name = body_data.get("name")
    user_result.email = body_data.get("email")
    user_result.password = body_data.get("password")

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