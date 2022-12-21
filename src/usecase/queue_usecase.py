from src.lib.model import Queue, db
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
from sqlalchemy.exc import IntegrityError, StatementError


class QueueUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality

    def get_queue_by_admin(self, admin_email: str, queue_id: int) -> dict:

        admin_result = self._db_postgre_functionality.get_admin_using_admin_email(
            admin_email
        )

        queue_result = self._db_postgre_functionality.get_queue_in_list(
            queue_id, admin_result.id
        )

        try:
            if len(queue_result) == 0:
                raise NotFoundError()
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_queue()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_queue()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = [convert_model_to_dict(queue) for queue in queue_result]

        return {"status_code": status_code, "data": data}

    def get_queue_by_user(self, user_email: str, queue_id: int) -> dict:

        user_result = self._db_postgre_functionality.get_user_using_user_email(
            user_email
        )

        queue_user_result = self._db_postgre_functionality.get_queue_user_using_user_id(
            user_result.id
        )

        queue_result = self._db_postgre_functionality.get_queue_in_list_by_user(
            queue_user_result, queue_id
        )

        try:
            if len(queue_user_result) == 0 or len(queue_result) == 0:
                raise NotFoundError()
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_queue_by_user()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_queue_by_user()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = [convert_model_to_dict(queue) for queue in queue_result]

        return {"status_code": status_code, "data": data}

    def post_queue(self, admin_email: str, body_data: dict) -> dict:

        admin_result = self._db_postgre_functionality.get_admin_using_admin_email(
            admin_email
        )

        try:
            queue = Queue(
                name=body_data.get("name"),
                description=body_data.get("description"),
                status=body_data.get("status"),
                admin_id=admin_result.id,
            )

            db.session.add(queue)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_queue()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_queue()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(queue)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def delete_queue(self, admin_email: str, queue_id: int) -> dict:

        admin_result = self._db_postgre_functionality.get_admin_using_admin_email(
            admin_email
        )

        queue_result = (
            self._db_postgre_functionality.get_queue_using_admin_id_and_queue_id(
                queue_id, admin_result.id
            )
        )

        try:
            if not queue_result:
                raise NotFoundError()

            db.session.delete(queue_result)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_queue()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_queue()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_queue()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def edit_queue(self, admin_email: str, queue_id: int, body_data: dict) -> dict:

        admin_result = self._db_postgre_functionality.get_admin_using_admin_email(
            admin_email
        )

        queue_result = (
            self._db_postgre_functionality.get_queue_using_admin_id_and_queue_id(
                queue_id, admin_result.id
            )
        )

        try:
            if not queue_result:
                raise NotFoundError()

            queue_result.name = body_data.get("name")
            queue_result.description = body_data.get("description")
            queue_result.status = body_data.get("status")

            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_queue()': {repr(e)}"
        except StatementError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_queue()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_queue()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_queue()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(queue_result)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}
