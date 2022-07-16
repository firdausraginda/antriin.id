from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import Queue, Admin, db
from src.auth.auth_admin import auth_admin


queue = Blueprint("queue", __name__, url_prefix="/api/v1/queue")

@queue.route("/", methods=["POST", "GET"])
@auth_admin.login_required
def post_and_get_queue():

    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()

    if request.method == "GET":
        
        queue_result = Queue.query.filter_by(admin_id=admin_result.id).all()

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
            short_url = body_data.get("short_url"),
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

@queue.get("/<int:id>")
@auth_admin.login_required
def get_queue(id):
    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()
    queue_result = Queue.query.filter_by(id=id,admin_id=admin_result.id).first()

    if not queue_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    return jsonify({
        "id": queue_result.id,
        "name": queue_result.name,
        "created_at": queue_result.created_at,
        "updated_at": queue_result.updated_at,
        "description": queue_result.description,
        "status": queue_result.status,
        "short_url": queue_result.short_url,
        "admin_id": queue_result.admin_id
    }), HTTP_200_OK
            
@queue.delete("/<int:id>")
@auth_admin.login_required
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
@queue.patch("/<int:id>")
@auth_admin.login_required
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