from flask import Blueprint, request, jsonify
from flasgger import swag_from


def process_queue_user(queue_user_usecase, admin_auth, user_auth):

    queue_user = Blueprint("queue_user", __name__, url_prefix="/api/v1/queue_user")

    @queue_user.get("/", defaults={"queue_user_id": None})
    @queue_user.get("/<int:queue_user_id>")
    @admin_auth.login_required
    @swag_from("../docs/queue_user/get_queue_user_using_auth_admin.yaml")
    @swag_from("../docs/queue_user/get_queue_user_by_id_using_auth_admin.yaml")
    def get_queue_user_by_auth_admin(queue_user_id):

        result = queue_user_usecase.get_queue_by_admin(
            admin_auth.current_user(), queue_user_id
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue_user.post("/")
    @admin_auth.login_required
    @swag_from("../docs/queue_user/post_queue_user_using_auth_admin.yaml")
    def post_queue_user_by_auth_admin():

        body_data = request.get_json()
        result = queue_user_usecase.post_queue_user_by_admin(
            admin_auth.current_user(), body_data
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue_user.post("/join_queue/<int:queue_id>")
    @user_auth.login_required
    @swag_from("../docs/queue_user/post_queue_user_by_id_using_auth_user.yaml")
    def post_queue_user_by_auth_user(queue_id):

        result = queue_user_usecase.post_queue_user_by_user(
            queue_id, user_auth.current_user()
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue_user.delete("/<int:queue_user_id>")
    @admin_auth.login_required
    @swag_from("../docs/queue_user/delete_queue_user_by_id_using_auth_admin.yaml")
    def delete_queue_user(queue_user_id):

        result = queue_user_usecase.delete_queue_user(
            admin_auth.current_user(), queue_user_id
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue_user.put("/<int:queue_user_id>")
    @admin_auth.login_required
    @swag_from("../docs/queue_user/edit_queue_user_by_id_using_auth_admin.yaml")
    def edit_queue_user(queue_user_id):

        body_data = request.get_json()
        result = queue_user_usecase.edit_queue_user(
            admin_auth.current_user(), queue_user_id, body_data
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    return queue_user
