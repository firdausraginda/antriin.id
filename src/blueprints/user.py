# from flask import Blueprint, request, jsonify
# from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
# from src.database import Admin, User, Queue, QueueUser, db
# from auth.auth_admin import auth


# user = Blueprint("user", __name__, url_prefix="/api/v1/user")

# @user.route("/", methods=["POST", "GET"])
# def post_and_get_user():

#     if request.method == "GET":

#         user_result = User.query.all()

#         data = []
#         for user in user_result:
#             data.append({
#                 "id": user.id,
#                 "name": user.name,
#                 "email": user.email,
#                 "password": user.password,
#                 "created_at": user.created_at
#             })
        
#         return jsonify({
#             "data": data
#         }), HTTP_200_OK
           
#     else:
#         body_data = request.get_json()

#         user = User(
#             name = body_data.get("name"),
#             email = body_data.get("email"),
#             password = body_data.get("password")
#         )

#         try:
#             db.session.add(user)
#             db.session.commit()
#         except:
#             db.session.rollback()
#             raise
        
#         return jsonify({
#             "name": body_data.get("name"),
#             "email": body_data.get("email"),
#             "password": body_data.get("password")
#         }), HTTP_201_CREATED

# @user.get("/<int:id>")
# def get_admin(id):

#     user_result = User.query.filter_by(id=id).first()

#     if not user_result:
#         return jsonify({
#             "message": "item not found!"
#         }), HTTP_404_NOT_FOUND
    
#     return jsonify({
#         "id": user_result.id,
#         "name": user_result.name,
#         "email": user_result.email,
#         "password": user_result.password,
#         "created_at": user_result.created_at
#     }), HTTP_200_OK

# @user.delete("/<int:id>")
# @auth.login_required
# def delete_admin(id):
#     admin_result = Admin.query.filter_by(email=auth.current_user()).first()
#     queue_result = Queue.query.filter_by(admin_id=admin_result.id).first()
#     queue_user_result = QueueUser.query.filter_by(queue_id=queue_result.id,user_id=id).all()

#     if not queue_user_result:
#         return jsonify({
#             "message": "item not found!"
#         }), HTTP_404_NOT_FOUND
    
#     try:
#         db.session.delete(admin_result)
#         db.session.commit()
#     except:
#         db.session.rollback()
#         raise
#     finally:
#         db.session.close()

#     return ({}), HTTP_204_NO_CONTENT

# @admin.put("/<int:id>")
# @admin.patch("/<int:id>")
# @auth.login_required
# def edit_admin(id):
#     super_admin_result = SuperAdmin.query.filter_by(email=auth.current_user()).first()
#     organization_result = Organization.query.filter_by(super_admin_id=super_admin_result.id).first()
#     admin_result = Admin.query.filter_by(id=id,organization_id=organization_result.id).first()

#     if not admin_result:
#         return jsonify({
#             "message": "item not found!"
#         }), HTTP_404_NOT_FOUND
    
#     body_data = request.get_json()
#     admin_result.name = body_data.get("name")
#     admin_result.email = body_data.get("email")
#     admin_result.password = body_data.get("password")

#     try:
#         db.session.commit()
#     except:
#         db.session.rollback()
#         raise
#     finally:
#         db.session.close()

#     return jsonify({
#         "name": body_data.get("name"),
#         "email": body_data.get("email"),
#         "password": body_data.get("password")
#     }), HTTP_200_OK