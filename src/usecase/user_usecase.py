from src.lib.model import Admin, User, db
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


class UserUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality

    def get_user_by_admin(self, admin_email: str, user_id: int) -> dict:

        admin_result = self._db_postgre_functionality.get_admin_using_admin_email(
            admin_email
        )

        queue_result = self._db_postgre_functionality.get_queue_using_admin_id(
            admin_result.id
        )

        queue_user_result = (
            self._db_postgre_functionality.get_queue_user_using_list_queue(queue_result)
        )

        user_result = self._db_postgre_functionality.get_user_in_list(
            queue_user_result, user_id
        )

        try:
            if not queue_result or len(queue_user_result) == 0 or len(user_result) == 0:
                raise NotFoundError()
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_user_by_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_user_by_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = [convert_model_to_dict(user) for user in user_result]

        return {"status_code": status_code, "data": data}

    def get_user_by_user(self, user_email: str) -> dict:

        user_result = User.query.filter_by(email=user_email).first()

        data = convert_model_to_dict(user_result)
        status_code = HTTP_200_OK

        return {"status_code": status_code, "data": data}

    def post_user(self, body_data: dict) -> dict:

        try:
            user = User(
                name=body_data.get("name"),
                email=body_data.get("email"),
                password=body_data.get("password"),
            )

            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_user_by_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_user_by_admin()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(user)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def delete_user_by_user(self, user_email: str) -> dict:

        user_result = User.query.filter_by(email=user_email).first()

        try:
            db.session.delete(user_result)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_user_by_user()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_user_by_user()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_user_by_user()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def edit_user_by_user(self, user_email: str, body_data: dict) -> dict:

        user_result = User.query.filter_by(email=user_email).first()

        try:
            user_result.name = body_data.get("name")
            user_result.email = body_data.get("email")
            user_result.password = body_data.get("password")

            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_user_by_user()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_user_by_user()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_user_by_user()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(user_result)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}
