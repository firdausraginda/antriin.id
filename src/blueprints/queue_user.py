import json
from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_302_FOUND
from src.database import Queue, QueueUser, Admin, User, db
from src.auth.auth_admin import auth_admin
from src.auth.auth_user import auth_user
from flasgger import swag_from


queue_user = Blueprint("queue_user", __name__, url_prefix="/api/v1/queue_user")

@queue_user.route("/", defaults={"id": None}, methods=["POST", "GET"], endpoint="without_id")
@queue_user.route("/<int:id>", methods=["POST", "GET"], endpoint="with_id")
@auth_admin.login_required
@swag_from("../docs/queue_user/get_queue_user.yaml", endpoint="queue_user.without_id", methods=["GET"])
@swag_from("../docs/queue_user/get_queue_user_by_id.yaml", endpoint="queue_user.with_id", methods=["GET"])
@swag_from("../docs/queue_user/post_queue_user_by_auth_admin.yaml", endpoint="queue_user.without_id", methods=["POST"])
def post_and_get_queue_user_by_auth_admin(id):

    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()

    if request.method == "GET":

        queue_result = Queue.query.filter_by(admin_id=admin_result.id).all()
        filters = (QueueUser.queue_id.in_([queue.id for queue in queue_result]),)
        if id:
            filters = filters + ((QueueUser.id == id),)
        queue_user_result = QueueUser.query.filter(*filters).all()

        if not queue_result or not queue_user_result:
            return jsonify({
                "message": "item not found!"
            }), HTTP_404_NOT_FOUND

        data = []
        for queue_user in queue_user_result:
            data.append({
                "id": queue_user.id,
                "status": queue_user.status,
                "created_at": queue_user.created_at,
                "updated_at": queue_user.updated_at,
                "queue_id": queue_user.queue_id,
                "user_id": queue_user.user_id
            })

        return jsonify({
            "data": data
        })
    
    else:

        body_data = request.get_json()

        queue_user = QueueUser(
            status = body_data.get("status"),
            queue_id = body_data.get("queue_id"),
            user_id = body_data.get("user_id")
        )

        queue_result = Queue.query.filter_by(id=queue_user.queue_id).first()
        user_result = User.query.filter_by(id=queue_user.user_id).first()

        if not queue_result or not user_result:
            return jsonify({
                "message": "queue or user not found!"
            }), HTTP_404_NOT_FOUND

        try:
            db.session.add(queue_user)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        
        return jsonify({
            "status": body_data.get("status"),
            "queue_id": body_data.get("queue_id"),
            "user_id": body_data.get("user_id")
        }), HTTP_201_CREATED

@queue_user.post("/join_queue/<int:id>")
@auth_user.login_required
@swag_from("../docs/queue_user/post_queue_user_by_auth_user.yaml")
def post_queue_user_by_auth_user(id):

    queue_result = Queue.query.filter_by(id=id).first()
    user_result = User.query.filter_by(email=auth_user.current_user()).first()
    queue_user_result = QueueUser.query.filter_by(queue_id=id,user_id=user_result.id).first()
    
    if not user_result or not queue_result:
        return jsonify({
            "message": "queue or user not found!"
        }), HTTP_404_NOT_FOUND
    elif queue_user_result:
        return jsonify({
            "message": "user already join this queue!"
        }), HTTP_302_FOUND

    queue_user = QueueUser(
        queue_id = id,
        user_id = user_result.id
    )

    try:
        db.session.add(queue_user)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    
    return jsonify({
        "queue_id": id,
        "user_id": user_result.id
    }), HTTP_201_CREATED

@queue_user.delete("/<int:id>")
@auth_admin.login_required
@swag_from("../docs/queue_user/delete_queue_user_by_id.yaml")
def delete_queue_user(id):
    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()
    queue_result = Queue.query.filter_by(admin_id=admin_result.id).all()
    queue_user_result = QueueUser.query.filter(QueueUser.queue_id.in_([queue.id for queue in queue_result]),QueueUser.id==id).first()

    if not queue_result or not queue_user_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    try:
        db.session.delete(queue_user_result)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return ({}), HTTP_204_NO_CONTENT

@queue_user.put("/<int:id>")
@auth_admin.login_required
@swag_from("../docs/queue_user/edit_queue_user_by_id.yaml")
def edit_queue_user(id):
    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()
    queue_result = Queue.query.filter_by(admin_id=admin_result.id).all()
    queue_user_result = QueueUser.query.filter(QueueUser.queue_id.in_([queue.id for queue in queue_result]),QueueUser.id==id).first()

    if not queue_result or not queue_user_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    body_data = request.get_json()

    queue_user_result.status = body_data.get("status")
    queue_user_result.queue_id = body_data.get("queue_id")
    queue_user_result.user_id = body_data.get("user_id")

    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return jsonify({
        "status": body_data.get("status"),
        "queue_id": body_data.get("queue_id"),
        "user_id": body_data.get("user_id")
    }), HTTP_200_OK