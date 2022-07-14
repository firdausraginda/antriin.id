import json
from flask import Blueprint, request, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from src.database import Queue, QueueUser, User, Admin, db
from src.auth.auth_admin import auth as auth_admin
from src.auth.auth_user import auth as auth_user


queue_user = Blueprint("queue_user", __name__, url_prefix="/api/v1/queue_user")

@queue_user.get("/")
@auth_admin.login_required
def get_queue_user():

    admin_result = Admin.query.filter_by(email=auth_admin.current_user()).first()
    queue_result = Queue.query.filter_by(admin_id=admin_result.id).all()
    queue_user_result = QueueUser.query.filter(QueueUser.queue_id.in_([queue.id for queue in queue_result])).all()

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