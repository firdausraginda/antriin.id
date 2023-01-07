from src.lib.model_v2 import SuperAdmin
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
from sqlmodel import Session


class SuperAdminUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality
        self._engine = self._db_postgre_functionality._engine

    def get_super_admin(self, super_admin_id: int) -> dict:

        session = Session(self._engine)

        super_admin_result = session.exec(
            self._db_postgre_functionality.get_super_admin_using_super_admin_id(
                super_admin_id
            )
        ).first()

        try:
            if not super_admin_result:
                raise NotFoundError()
        except NotFoundError as e:
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_super_admin()': {repr(e)}"
        except Exception as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_super_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(super_admin_result)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def post_super_admin(self, body_data: dict) -> dict:

        super_admin = SuperAdmin(
            name=body_data.get("name"),
            email=body_data.get("email"),
            password=body_data.get("password"),
        )

        session = Session(self._engine)

        try:
            session.add(super_admin)
        except IntegrityError as e:
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_super_admin()': {repr(e)}"
        except Exception as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_super_admin()': {repr(e)}"
        else:
            session.commit()
            session.flush()
            session.refresh(super_admin)
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(super_admin)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def delete_super_admin(self, super_admin_id: int) -> dict:

        session = Session(self._engine)

        super_admin_result = session.exec(
            self._db_postgre_functionality.get_super_admin_using_super_admin_id(
                super_admin_id
            )
        ).first()

        try:
            if not super_admin_result:
                raise NotFoundError()

            session.delete(super_admin_result)
        except IntegrityError as e:
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_super_admin()': {repr(e)}"
        except NotFoundError as e:
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_super_admin()': {repr(e)}"
        except Exception as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_super_admin()': {repr(e)}"
        else:
            session.commit()
            session.flush()
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def edit_super_admin(self, super_admin_id: int, body_data: dict) -> dict:

        session = Session(self._engine)

        super_admin_result = session.exec(
            self._db_postgre_functionality.get_super_admin_using_super_admin_id(
                super_admin_id
            )
        ).first()

        try:
            if not super_admin_result:
                raise NotFoundError()

            super_admin_result.name = body_data.get("name")
            super_admin_result.email = body_data.get("email")
            super_admin_result.password = body_data.get("password")

            session.commit()
            session.flush()
        except IntegrityError as e:
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_super_admin()': {repr(e)}"
        except NotFoundError as e:
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_super_admin()': {repr(e)}"
        except Exception as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_super_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(super_admin_result)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}
