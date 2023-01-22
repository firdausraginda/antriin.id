from flask import Blueprint, request, jsonify
from flasgger import swag_from


def process_queue(queue_usecase, admin_auth, user_auth):

    queue = Blueprint("queue", __name__, url_prefix="/api/v1/queue")

    @queue.get("/", defaults={"queue_id": None}, endpoint="get_by_admin_without_id")
    @queue.get("/<int:queue_id>", endpoint="get_by_admin_with_id")
    @admin_auth.login_required
    @swag_from(
        "../docs/queue/get_queue_using_auth_admin.yaml",
        endpoint="queue.get_by_admin_without_id",
    )
    @swag_from(
        "../docs/queue/get_queue_by_id_using_auth_admin.yaml",
        endpoint="queue.get_by_admin_with_id",
    )
    def get_queue_auth_admin(queue_id):

        result = queue_usecase.get_queue_by_admin(admin_auth.current_user(), queue_id)

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue.get("/list/", defaults={"queue_id": None}, endpoint="get_by_user_without_id")
    @queue.get("/list/<int:queue_id>", endpoint="get_by_user_with_id")
    @user_auth.login_required
    @swag_from(
        "../docs/queue/get_queue_using_auth_user.yaml",
        endpoint="queue.get_by_user_without_id",
    )
    @swag_from(
        "../docs/queue/get_queue_by_id_using_auth_user.yaml",
        endpoint="queue.get_by_user_with_id",
    )
    def get_queue_by_auth_user(queue_id):

        result = queue_usecase.get_queue_by_user(admin_auth.current_user(), queue_id)

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue.post("/")
    @admin_auth.login_required
    @swag_from("../docs/queue/post_queue_using_auth_admin.yaml")
    def post_queue():

        body_data = request.get_json()
        result = queue_usecase.post_queue(admin_auth.current_user(), body_data)

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue.post("/next_queue_number/<int:queue_id>")
    @admin_auth.login_required
    @swag_from("../docs/queue/increment_queue_number_using_auth_admin.yaml")
    def increment_queue_number(queue_id):

        result = queue_usecase.increment_queue_number(
            admin_auth.current_user(), queue_id
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue.post("/previous_queue_number/<int:queue_id>")
    @admin_auth.login_required
    @swag_from("../docs/queue/decrement_queue_number_using_auth_admin.yaml")
    def decrement_queue_number(queue_id):

        result = queue_usecase.decrement_queue_number(
            admin_auth.current_user(), queue_id
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue.delete("/<int:queue_id>")
    @admin_auth.login_required
    @swag_from("../docs/queue/delete_queue_by_id_using_auth_admin.yaml")
    def delete_queue(queue_id):

        result = queue_usecase.delete_queue(admin_auth.current_user(), queue_id)

        return jsonify({"data": result["data"]}), result["status_code"]

    @queue.put("/<int:queue_id>")
    @admin_auth.login_required
    @swag_from("../docs/queue/edit_queue_by_id_using_auth_admin.yaml")
    def edit_queue(queue_id):

        body_data = request.get_json()
        result = queue_usecase.edit_queue(
            admin_auth.current_user(), queue_id, body_data
        )

        return jsonify({"data": result["data"]}), result["status_code"]

    return queue
