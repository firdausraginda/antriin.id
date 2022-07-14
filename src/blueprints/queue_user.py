from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import QueueUser, User, Admin, db
from src.auth.auth_admin import auth


queue_user = Blueprint("queue_user", __name__, url_prefix="/api/v1/queue_user")

@queue_user.get("/<int:queue_id>")
@auth.login_required
def get_queue_user(queue_id):

    user_result = User.query.filter_by(email=auth.current_user()).first()
    queue_user_result = QueueUser.query.filter_by(user_id=user_result.id).all()

    data = []
    for queue_user in queue_user_result:
        data.append({
            "id": queue_user.id,
            "status": queue_user.status,
            "created_at": queue_user.created_at,
            "updated_at": queue_user.updated_at,
            "queue_id": queue_id,
            "user_id": user_result.id
        })
    
    return jsonify({
        "data": data
    }), HTTP_200_OK

@queue_user.post("/<int:queue_id>")
@auth.login_required
def post_queue_user(queue_id):

    user_result = User.query.filter_by(email=auth.current_user()).first()
    queue_user_result = QueueUser.query.filter_by(user_id=user_result.id).all()

    body_data = request.get_json()

    queue_user = QueueUser(
        status = body_data.get("status"),
        queue_id = queue_id,
        user_id = queue_user_result.id
    )

    try:
        db.session.add(queue_user)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    
    return jsonify({
        "status": queue_user.status,
        "queue_id": queue_user.queue_id,
        "user_id": queue_user.user_id
    }), HTTP_201_CREATED

@queue_user.get("/<int:id>")
@auth.login_required
def get_queue_user(id):
    user_result = User.query.filter_by(email=auth.current_user()).first()
    queue_user_result = QueueUser.query.filter_by(id=id,user_id=user_result.id).all()

    if not queue_user_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    return jsonify({
        "id": queue_user_result.id,
        "name": queue_user_result.name,
        "created_at": queue_user_result.created_at,
        "updated_at": queue_user_result.updated_at,
        "description": queue_user_result.description,
        "status": queue_user_result.status,
        "short_url": queue_user_result.short_url,
        "admin_id": queue_user_result.admin_id
    }), HTTP_200_OK

@queue_user.delete("/<int:id>")
@auth.login_required
def delete_queue_user(id):
    admin_result = Admin.query.filter_by(email=auth.current_user()).first()
    queue_user_result = QueueUser.query.filter_by(id=id,admin_id=admin_result.id).first()

    if not queue_user_result:
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
@queue_user.patch("/<int:id>")
@auth.login_required
def edit_queue_user(id):
    admin_result = Admin.query.filter_by(email=auth.current_user()).first()
    queue_user_result = QueueUser.query.filter_by(id=id,admin_id=admin_result.id).first()

    if not queue_user_result:
        return jsonify({
            "message": "item not found!"
        }), HTTP_404_NOT_FOUND
    
    body_data = request.get_json()

    queue_user_result.status = body_data.get("status")

    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return jsonify({
        "status": body_data.get("status")
    }), HTTP_200_OK