from src.lib.model_v2 import Admin
from src.lib.custom_exception import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.lib.custom_exception import NotFoundError
from src.lib.function import convert_model_to_dict, update_existing_data
from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from sqlalchemy.exc import IntegrityError


class AdminUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality

    def get_admin(self, admin_email: str) -> dict:
        """get admin data using admin_email"""

        session = self._db_postgre_functionality.start_session()

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        session.close()

        data = convert_model_to_dict(admin_result)
        status_code = HTTP_200_OK

        return {"status_code": status_code, "data": data}

    def post_admin(self, body_data: dict) -> dict:
        """insert admin data using"""

        session = self._db_postgre_functionality.start_session()

        try:
            admin = Admin.validate(
                {
                    "name": body_data.get("name"),
                    "email": body_data.get("email"),
                    "password": body_data.get("password"),
                }
            )

            session.add(admin)
            session.commit()
            session.refresh(admin)
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_admin()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_admin()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(admin)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def delete_admin(self, admin_email: str) -> dict:
        """delete admin data using admin_email"""

        session = self._db_postgre_functionality.start_session()

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        try:
            session.delete(admin_result)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_admin()': {repr(e)}"
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_admin()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_admin()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def edit_admin(self, admin_email: str, body_data: dict) -> dict:
        """edit admin data using admin_email and admin_id"""

        session = self._db_postgre_functionality.start_session()

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        try:
            # update existing admin with updated data
            update_existing_data(admin_result, body_data)

            # validate updated admin
            Admin.validate({**convert_model_to_dict(admin_result)})

            session.add(admin_result)
            session.commit()
            session.refresh(admin_result)
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_admin()': {repr(e)}"
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_admin()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(admin_result)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}
