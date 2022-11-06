from flask import request
from src.lib.model import SuperAdmin, db
from src.lib.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

class SuperAdminUsecase:

    def __init__(self, db_postgre_functionality) -> None:
        
        self._db_postgre_functionality = db_postgre_functionality
    
    def get_super_admin(self, super_admin_id):

        super_admin_result = self._db_postgre_functionality.get_super_admin_using_super_admin_id(super_admin_id, False)

        data = []
        for super_admin in super_admin_result:
            data.append({
                "id": super_admin.id,
                "name": super_admin.name,
                "email": super_admin.email,
                "password": super_admin.password,
                "created_at": super_admin.created_at
            })

        if not super_admin_result:
            message = HTTP_404_NOT_FOUND
            data = "item not found!"
        else:
            message = HTTP_200_OK
            data = data

        response_result = {
            "message": message,
            "data": data
        }

        return response_result
    
    def post_super_admin(self, body_data):

        super_admin = SuperAdmin(
            name = body_data.get("name"),
            email = body_data.get("email"),
            password = body_data.get("password")
        )

        try:
            db.session.add(super_admin)
            db.session.commit()

            message = HTTP_201_CREATED
            data = {
                "name": body_data.get("name"),
                "email": body_data.get("email"),
                "password": body_data.get("password")
            }
        except:
            db.session.rollback()

            message = HTTP_400_BAD_REQUEST
            data = "bad request!"

            raise
        finally:
            db.session.close()

        return {
            "message": message,
            "data": data
        }