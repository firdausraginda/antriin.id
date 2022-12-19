from src.lib.model import SuperAdmin, db
from src.lib.custom_exception import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.lib.custom_exception import NotFoundError
from src.lib.function import convert_model_to_dict
from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from sqlalchemy.exc import IntegrityError


class SuperAdminUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality

    def get_super_admin(self, super_admin_id: int) -> dict:

        super_admin_result = (
            self._db_postgre_functionality.get_super_admin_using_super_admin_id(
                super_admin_id
            )
        )

        try:
            if not super_admin_result:
                raise NotFoundError(super_admin_id)
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_super_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_super_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(super_admin_result)

        return {"status_code": status_code, "data": data}

    def post_super_admin(self, body_data: dict) -> dict:

        super_admin = SuperAdmin(
            name=body_data.get("name"),
            email=body_data.get("email"),
            password=body_data.get("password"),
        )

        try:
            db.session.add(super_admin)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_super_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_super_admin()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(super_admin)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def delete_super_admin(self, super_admin_id: int) -> dict:

        super_admin_result = (
            self._db_postgre_functionality.get_super_admin_using_super_admin_id(
                super_admin_id
            )
        )

        try:
            if not super_admin_result:
                raise NotFoundError(super_admin_id)

            db.session.delete(super_admin_result)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_super_admin()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_super_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_super_admin()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def edit_super_admin(self, super_admin_id: int, body_data: dict) -> dict:

        super_admin_result = (
            self._db_postgre_functionality.get_super_admin_using_super_admin_id(
                super_admin_id
            )
        )

        try:
            if not super_admin_result:
                raise NotFoundError(super_admin_id)

            super_admin_result.name = body_data.get("name")
            super_admin_result.email = body_data.get("email")
            super_admin_result.password = body_data.get("password")

            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_super_admin()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_super_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_super_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(super_admin_result)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}
