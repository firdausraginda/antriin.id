from src.lib.model_v2 import QueueUser
from src.lib.custom_exception import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.lib.custom_exception import NotFoundError, DuplicateItemByForeignKey
from src.lib.function import convert_model_to_dict, update_existing_data
from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from sqlalchemy.exc import IntegrityError, StatementError
from sqlmodel import Session


class QueueUserUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality

    def get_queue_by_admin(self, admin_email: str, queue_user_id: int) -> dict:
        """get queue data using admin_email and queue_user_id"""

        session = self._db_postgre_functionality.start_session()

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        queue_result = session.exec(
            self._db_postgre_functionality.get_queue_using_admin_id(admin_result.id)
        ).all()

        queue_user_result = session.exec(
            self._db_postgre_functionality.get_queue_user_in_list(
                queue_result, queue_user_id
            )
        ).all()

        try:
            if len(queue_result) == 0 or len(queue_user_result) == 0:
                raise NotFoundError()
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_queue_by_admin()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_queue_by_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = [
                convert_model_to_dict(queue_user) for queue_user in queue_user_result
            ]
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def post_queue_user_by_admin(self, admin_email: str, body_data: dict) -> dict:
        """insert queue user data by admin"""

        session = self._db_postgre_functionality.start_session()

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        queue_admin_result = session.exec(
            self._db_postgre_functionality.get_queue_using_admin_id(admin_result.id)
        ).all()

        try:
            queue_user = QueueUser.validate(
                {
                    "status": body_data.get("status"),
                    "queue_id": body_data.get("queue_id"),
                    "user_id": body_data.get("user_id"),
                }
            )

            queue_result = session.exec(
                self._db_postgre_functionality.get_queue_using_queue_id(
                    queue_user.queue_id
                )
            ).first()

            user_result = session.exec(
                self._db_postgre_functionality.get_user_using_user_id(
                    queue_user.user_id
                )
            ).first()

            if (
                not queue_result
                or not user_result
                or not any(
                    [
                        queue_user.queue_id == queue_existing.id
                        for queue_existing in queue_admin_result
                    ]
                )
            ):
                raise NotFoundError()
            else:
                queue_user_result = session.exec(
                    self._db_postgre_functionality.get_queue_user_using_queue_id_and_user_id(
                        queue_result.id, user_result.id
                    )
                ).first()
                if queue_user_result:
                    raise DuplicateItemByForeignKey()

            session.add(queue_user)
            session.commit()
            session.refresh(queue_user)
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'post_queue_user_by_admin()': {repr(e)}"
        except (IntegrityError, DuplicateItemByForeignKey) as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_queue_user_by_admin()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_queue_user_by_admin()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(queue_user)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def post_queue_user_by_user(self, queue_id: int, user_email: str) -> dict:
        """insert queue user data by user"""

        session = self._db_postgre_functionality.start_session()

        queue_result = session.exec(
            self._db_postgre_functionality.get_queue_using_queue_id(queue_id)
        ).first()

        user_result = session.exec(
            self._db_postgre_functionality.get_user_using_user_email(user_email)
        ).first()

        try:
            if not queue_result or not user_result:
                raise NotFoundError()
            else:
                queue_user_result = session.exec(
                    self._db_postgre_functionality.get_queue_user_using_queue_id_and_user_id(
                        queue_result.id, user_result.id
                    )
                ).first()
                if queue_user_result:
                    raise DuplicateItemByForeignKey()

            queue_user = QueueUser.validate(
                {"queue_id": queue_id, "user_id": user_result.id}
            )

            session.add(queue_user)
            session.commit()
            session.refresh(queue_user)
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'post_queue_user_by_user()': {repr(e)}"
        except (IntegrityError, DuplicateItemByForeignKey) as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_queue_user_by_user()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_queue_user_by_user()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(queue_user)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def delete_queue_user(self, admin_email: str, queue_user_id: int) -> dict:
        """delete queue user data using admin_email and queue_user_id"""

        session = self._db_postgre_functionality.start_session()

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        queue_result = session.exec(
            self._db_postgre_functionality.get_queue_using_admin_id(admin_result.id)
        ).all()

        queue_user_result = session.exec(
            self._db_postgre_functionality.get_queue_user_using_list_queue_and_queue_user_id(
                queue_result, queue_user_id
            )
        ).first()

        try:
            if len(queue_result) == 0 or not queue_user_result:
                raise NotFoundError()

            session.delete(queue_user_result)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_queue_user()': {repr(e)}"
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_queue_user()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_queue_user()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def edit_queue_user(
        self, admin_email: str, queue_user_id: int, body_data: dict
    ) -> dict:
        """edit queue user data using admin_email and queue_user_id"""

        session = self._db_postgre_functionality.start_session()

        admin_result = session.exec(
            self._db_postgre_functionality.get_admin_using_admin_email(admin_email)
        ).first()

        queue_result = session.exec(
            self._db_postgre_functionality.get_queue_using_admin_id(admin_result.id)
        ).all()

        try:
            if len(queue_result) == 0:
                raise NotFoundError()
            else:
                queue_user_result = session.exec(
                    self._db_postgre_functionality.get_queue_user_using_list_queue_and_queue_user_id(
                        queue_result, queue_user_id
                    )
                ).first()

                if not queue_user_result:
                    raise NotFoundError()

            # update existing queue user with updated data
            update_existing_data(queue_user_result, body_data)

            # validate updated queue user
            QueueUser.validate({**convert_model_to_dict(queue_user_result)})

            session.add(queue_user_result)
            session.commit()
            session.refresh(queue_user_result)
        except (StatementError, IntegrityError) as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_queue_user()': {repr(e)}"
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_queue_user()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_queue_user()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(queue_user_result)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}
