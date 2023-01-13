from src.lib.model_v2 import Queue
from src.lib.custom_exception import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.lib.custom_exception import NotFoundError
from src.lib.function import convert_model_to_dict, generate_short_url
from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from sqlalchemy.exc import IntegrityError, StatementError
from sqlmodel import Session


class QueueUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality
        self._engine = self._db_postgre_functionality._engine

    def get_queue_by_admin(self, admin_email: str, queue_id: int) -> dict:

        session = Session(self._engine)

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        queue_result = session.exec(
            self._db_postgre_functionality.get_queue_in_list_by_admin(
                queue_id, admin_result.id
            )
        ).all()

        try:
            if len(queue_result) == 0:
                raise NotFoundError()
        except NotFoundError as e:
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_queue()': {repr(e)}"
        except Exception as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_queue()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = [convert_model_to_dict(queue) for queue in queue_result]
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def get_queue_by_user(self, user_email: str, queue_id: int) -> dict:

        session = Session(self._engine)

        user_result = session.exec(
            self._db_postgre_functionality.get_user_using_user_email(user_email)
        ).first()

        queue_user_result = session.exec(
            self._db_postgre_functionality.get_queue_user_using_user_id(user_result.id)
        ).all()

        queue_result = session.exec(
            self._db_postgre_functionality.get_queue_in_list_by_user(
                queue_user_result, queue_id
            )
        ).all()

        try:
            if len(queue_user_result) == 0 or len(queue_result) == 0:
                raise NotFoundError()
        except NotFoundError as e:
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_queue_by_user()': {repr(e)}"
        except Exception as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_queue_by_user()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = [convert_model_to_dict(queue) for queue in queue_result]
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def post_queue(self, admin_email: str, body_data: dict) -> dict:

        session = Session(self._engine)

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        # generate short_url that not exist in DB yet
        while True:
            short_url = generate_short_url()
            if not session.exec(
                self._db_postgre_functionality.get_queue_using_short_url(short_url)
            ).first():
                break

        try:
            queue = Queue.validate(
                {
                    "name": body_data.get("name"),
                    "description": body_data.get("description"),
                    "status": body_data.get("status"),
                    "short_url": short_url,
                    "admin_id": admin_result.id,
                }
            )

            session.add(queue)
            session.commit()
            session.flush()
        except (StatementError, IntegrityError) as e:
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_queue()': {repr(e)}"
        except Exception as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_queue()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(queue)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def delete_queue(self, admin_email: str, queue_id: int) -> dict:

        session = Session(self._engine)

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        queue_result = session.exec(
            self._db_postgre_functionality.get_queue_using_admin_id_and_queue_id(
                queue_id, admin_result.id
            )
        ).first()

        try:
            if not queue_result:
                raise NotFoundError()

            session.delete(queue_result)
            session.commit()
            session.flush()
        except IntegrityError as e:
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_queue()': {repr(e)}"
        except NotFoundError as e:
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_queue()': {repr(e)}"
        except Exception as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_queue()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def edit_queue(self, admin_email: str, queue_id: int, body_data: dict) -> dict:

        session = Session(self._engine)

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        queue_result = session.exec(
            self._db_postgre_functionality.get_queue_using_admin_id_and_queue_id(
                queue_id, admin_result.id
            )
        ).first()

        try:
            if not queue_result:
                raise NotFoundError()

            # update existing queue with updated data
            [setattr(queue_result, key, val) for key, val in body_data.items()]

            # validate updated queue
            Queue.validate({**convert_model_to_dict(queue_result)})

            session.add(queue_result)
            session.commit()
            session.refresh(queue_result)
            session.flush()
        except (StatementError, IntegrityError) as e:
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_queue()': {repr(e)}"
        except NotFoundError as e:
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_queue()': {repr(e)}"
        except Exception as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_queue()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(queue_result)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}
