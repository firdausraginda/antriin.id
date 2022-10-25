from flask import Blueprint, request, jsonify
from src.lib.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import Queue, Admin, QueueUser, User, db
from src.auth.auth_admin import auth_admin
from src.auth.auth_user import auth_user
from flasgger import swag_from


queue = Blueprint("queue", __name__, url_prefix="/api/v1/queue")

@queue.route("/", defaults={"id": None}, methods=["POST", "GET"], endpoint="without_id")
@queue.route("/<int:id>", methods=["POST", "GET"], endpoint="with_id")
@auth_admin.login_required
@swag_from("../docs/queue/get_queue_using_auth_admin.yaml", endpoint="queue.without_id", methods=["GET"])
@swag_from("../docs/queue/get_queue_by_id_using_auth_admin.yaml", endpoint="queue.with_id", methods=["GET"])
@swag_from("../docs/queue/post_queue_using_auth_admin.yaml", endpoint="queue.without_id", methods=["POST"])
def post_and_get_queue_by_auth_admin(id):

    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()

    if request.method == "GET":

        filters = (Queue.admin_id == admin_result.id,)
        if id:
            filters = filters + ((Queue.id == id),)
        queue_result = Queue.query.filter(*filters).all()

        if not queue_result:
            return jsonify({
                "message": "item not found!"
            }), HTTP_404_NOT_FOUND

        data = []
        for queue in queue_result:
            data.append({
                "id": queue.id,
                "name": queue.name,
                "created_at": queue.created_at,
                "updated_at": queue.updated_at,
                "description": queue.description,
                "status": queue.status,
                "short_url": queue.short_url,
                "admin_id": queue.admin_id
            })
        
        return jsonify({
            "data": data
        }), HTTP_200_OK

    else:
        body_data = request.get_json()

        queue = Queue(
            name = body_data.get("name"),
            description = body_data.get("description"),
            status = body_data.get("status"),
            admin_id = admin_result.id
        )

        try:
            db.session.add(queue)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        
        return jsonify({
            "name": body_data.get("name"),
            "description": body_data.get("description"),
            "status": body_data.get("status"),
            "admin_id": admin_result.id
        }), HTTP_201_CREATED

@queue.get("/list")
@auth_user.login_required
@swag_from("../docs/queue/get_queue_using_auth_user.yaml")
def get_queue_by_auth_user():
    user_result = User.query.filter_by(email=auth_user.current_user()).first()
    queue_user_result = QueueUser.query.filter_by(user_id=user_result.id).all()
    queue_result = Queue.query.filter(Queue.id.in_([queue_user.queue_id for queue_user in queue_user_result])).all()

    data = []
    for queue in queue_result:
        data.append({
            "id": queue.id,
            "name": queue.name,
            "created_at": queue.created_at,
            "updated_at": queue.updated_at,
            "description": queue.description,
            "status": queue.status,
            "short_url": queue.short_url,
            "admin_id": queue.admin_id
        })
    
    return jsonify({
        "data": data
    }), HTTP_200_OK

@queue.delete("/<int:id>")
@auth_admin.login_required
@swag_from("../docs/queue/delete_queue_by_id_using_auth_admin.yaml")
def delete_queue(id):
    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()
    queue_result = Queue.query.filter_by(id=id,admin_id=admin_result.id).first()

    if not queue_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    try:
        db.session.delete(queue_result)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return ({}), HTTP_204_NO_CONTENT

@queue.put("/<int:id>")
@auth_admin.login_required
@swag_from("../docs/queue/edit_queue_by_id_using_auth_admin.yaml")
def edit_queue(id):
    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()
    queue_result = Queue.query.filter_by(id=id,admin_id=admin_result.id).first()

    if not queue_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    body_data = request.get_json()

    queue_result.name = body_data.get("name")
    queue_result.description = body_data.get("description")
    queue_result.status = body_data.get("status")

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
        "status": body_data.get("status")
    }), HTTP_200_OK