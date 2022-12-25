from src.lib.model import Queue, QueueUser, User, db
from src.lib.custom_exception import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.lib.custom_exception import NotFoundError, DuplicateItemByForeignKey
from src.lib.function import convert_model_to_dict
from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from sqlalchemy.exc import IntegrityError, StatementError


class QueueUserUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality

    def get_queue_by_admin(self, admin_email: str, queue_user_id: int) -> dict:

        admin_result = self._db_postgre_functionality.get_admin_using_admin_email(
            admin_email
        )

        queue_result = self._db_postgre_functionality.get_queue_using_admin_id(
            admin_result.id
        )

        queue_user_result = self._db_postgre_functionality.get_queue_user_in_list(
            queue_result, queue_user_id
        )

        try:
            if len(queue_result) == 0 or len(queue_user_result) == 0:
                raise NotFoundError()
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_queue_by_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_queue_by_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = [
                convert_model_to_dict(queue_user) for queue_user in queue_user_result
            ]

        return {"status_code": status_code, "data": data}

    def post_queue_user_by_admin(self, body_data: dict) -> dict:

        queue_user = QueueUser(
            status=body_data.get("status"),
            queue_id=body_data.get("queue_id"),
            user_id=body_data.get("user_id"),
        )

        queue_result = self._db_postgre_functionality.get_queue_using_queue_id(
            queue_user.queue_id
        )

        user_result = self._db_postgre_functionality.get_user_using_user_id(
            queue_user.user_id
        )

        queue_user_result = (
            self._db_postgre_functionality.get_queue_user_using_queue_id_and_user_id(
                queue_result.id, user_result.id
            )
        )

        try:
            if not queue_result or not user_result:
                raise NotFoundError()
            elif queue_user_result:
                raise DuplicateItemByForeignKey()

            db.session.add(queue_user)
            db.session.commit()
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'post_queue_user_by_admin()': {repr(e)}"
        except DuplicateItemByForeignKey as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_queue_user_by_admin()': {repr(e)}"
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_queue_user_by_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_queue_user_by_admin()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(queue_user)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def post_queue_user_by_user(self, queue_id: int, user_email: str) -> dict:

        queue_result = self._db_postgre_functionality.get_queue_using_queue_id(queue_id)

        user_result = self._db_postgre_functionality.get_user_using_user_email(
            user_email
        )

        queue_user_result = (
            self._db_postgre_functionality.get_queue_user_using_queue_id_and_user_id(
                queue_result.id, user_result.id
            )
        )

        try:
            if not queue_result or not user_result:
                raise NotFoundError()
            elif queue_user_result:
                raise DuplicateItemByForeignKey()

            queue_user = QueueUser(queue_id=queue_id, user_id=user_result.id)

            db.session.add(queue_user)
            db.session.commit()
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'post_queue_user_by_user()': {repr(e)}"
        except DuplicateItemByForeignKey as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_queue_user_by_user()': {repr(e)}"
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_queue_user_by_user()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_queue_user_by_user()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(queue_user)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def delete_queue_user(self, admin_email: str, queue_user_id: int) -> dict:

        admin_result = self._db_postgre_functionality.get_admin_using_admin_email(
            admin_email
        )

        queue_result = self._db_postgre_functionality.get_queue_using_admin_id(
            admin_result.id
        )

        queue_user_result = self._db_postgre_functionality.get_queue_user_using_list_queue_and_queue_user_id(
            queue_result, queue_user_id
        )

        try:
            if len(queue_result) == 0 or not queue_user_result:
                raise NotFoundError()

            db.session.delete(queue_user_result)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_queue_user()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_queue_user()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_queue_user()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def edit_queue_user(
        self, admin_email: str, queue_user_id: int, body_data: dict
    ) -> dict:

        admin_result = self._db_postgre_functionality.get_admin_using_admin_email(
            admin_email
        )

        queue_result = self._db_postgre_functionality.get_queue_using_admin_id(
            admin_result.id
        )

        queue_user_result = self._db_postgre_functionality.get_queue_user_using_list_queue_and_queue_user_id(
            queue_result, queue_user_id
        )

        try:
            if not queue_result or not queue_user_result:
                raise NotFoundError()

            queue_user_result.status = body_data.get("status")
            queue_user_result.queue_id = body_data.get("queue_id")
            queue_user_result.user_id = body_data.get("user_id")

            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_queue_user()': {repr(e)}"
        except StatementError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_queue_user()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_queue_user()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_queue_user()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(queue_user_result)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}
