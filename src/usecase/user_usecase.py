from src.lib.model_v2 import User
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
from sqlmodel import Session


class UserUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality

    def get_user_by_admin(self, admin_email: str, user_id: int) -> dict:
        """get user data using admin_email and user_id by admin"""

        session = self._db_postgre_functionality.start_session()

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        queue_result = session.exec(
            self._db_postgre_functionality.get_queue_using_admin_id(admin_result.id)
        ).all()

        queue_user_result = session.exec(
            self._db_postgre_functionality.get_queue_user_using_list_queue(queue_result)
        ).all()

        user_result = session.exec(
            self._db_postgre_functionality.get_user_in_list(queue_user_result, user_id)
        ).all()

        try:
            if (
                len(queue_result) == 0
                or len(queue_user_result) == 0
                or len(user_result) == 0
            ):
                raise NotFoundError()
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_user_by_admin()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_user_by_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = [convert_model_to_dict(user) for user in user_result]
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def get_user_by_user(self, user_email: str) -> dict:
        """get user data using user_email by user"""

        session = self._db_postgre_functionality.start_session()

        user_result = session.exec(
            self._db_postgre_functionality.get_user_using_user_email(user_email)
        ).first()

        session.close()

        data = convert_model_to_dict(user_result)
        status_code = HTTP_200_OK

        return {"status_code": status_code, "data": data}

    def post_user(self, body_data: dict) -> dict:
        """insert user data"""

        session = self._db_postgre_functionality.start_session()

        try:
            user = User.validate(
                {
                    "name": body_data.get("name"),
                    "email": body_data.get("email"),
                    "password": body_data.get("password"),
                }
            )

            session.add(user)
            session.commit()
            session.refresh(user)
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_user_by_admin()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_user_by_admin()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(user)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def delete_user_by_user(self, user_email: str) -> dict:
        """delete user data using user_email by user"""

        session = self._db_postgre_functionality.start_session()

        user_result = session.exec(
            self._db_postgre_functionality.get_user_using_user_email(user_email)
        ).first()

        try:
            session.delete(user_result)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_user_by_user()': {repr(e)}"
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_user_by_user()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_user_by_user()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def edit_user_by_user(self, user_email: str, body_data: dict) -> dict:
        """edit user data using user_email by user"""

        session = self._db_postgre_functionality.start_session()

        user_result = session.exec(
            self._db_postgre_functionality.get_user_using_user_email(user_email)
        ).first()

        try:
            # update existing user with updated data
            update_existing_data(user_result, body_data)

            # validate updated user
            User.validate({**convert_model_to_dict(user_result)})

            session.add(user_result)
            session.commit()
            session.refresh(user_result)
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_user_by_user()': {repr(e)}"
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_user_by_user()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_user_by_user()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(user_result)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}
