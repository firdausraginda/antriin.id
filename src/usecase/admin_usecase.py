from src.lib.model import Admin, db
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


class AdminUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality

    def get_admin(self, super_admin_email: str, admin_id: int = None) -> dict:

        super_admin_result = self._db_postgre_functionality.get_super_admin_using_email(
            super_admin_email
        )

        org_result = self._db_postgre_functionality.get_org_using_super_admin_id(
            super_admin_result.id
        )

        admin_result = self._db_postgre_functionality.get_admin_using_org_id(
            org_result.id
        )

        try:
            if not org_result or len(admin_result) == 0:
                raise NotFoundError()
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = [convert_model_to_dict(admin) for admin in admin_result]

        return {"status_code": status_code, "data": data}

    def post_admin(self, super_admin_email: str, body_data: dict) -> dict:

        super_admin_result = self._db_postgre_functionality.get_super_admin_using_email(
            super_admin_email
        )

        org_result = self._db_postgre_functionality.get_org_using_super_admin_id(
            super_admin_result.id
        )

        try:
            if not org_result:
                raise NotFoundError()

            admin = Admin(
                name=body_data.get("name"),
                email=body_data.get("email"),
                password=body_data.get("password"),
                organization_id=org_result.id,
            )

            db.session.add(admin)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_admin()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(admin)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def delete_admin(self, super_admin_email: str, admin_id: int) -> dict:

        super_admin_result = self._db_postgre_functionality.get_super_admin_using_email(
            super_admin_email
        )

        org_result = self._db_postgre_functionality.get_org_using_super_admin_id(
            super_admin_result.id
        )

        admin_result = (
            self._db_postgre_functionality.get_admin_using_org_id_and_admin_id(
                org_result.id, admin_id
            )
        )

        try:
            if not org_result or not admin_result:
                raise NotFoundError()

            db.session.delete(admin_result)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_admin()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_admin()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}

    def edit_admin(
        self, super_admin_email: str, admin_id: int, body_data: dict
    ) -> dict:

        super_admin_result = self._db_postgre_functionality.get_super_admin_using_email(
            super_admin_email
        )

        org_result = self._db_postgre_functionality.get_org_using_super_admin_id(
            super_admin_result.id
        )

        admin_result = (
            self._db_postgre_functionality.get_admin_using_org_id_and_admin_id(
                org_result.id, admin_id
            )
        )

        try:
            if not org_result or not admin_result:
                raise NotFoundError()

            admin_result.name = body_data.get("name")
            admin_result.email = body_data.get("email")
            admin_result.password = body_data.get("password")

            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_admin()': {repr(e)}"
        except NotFoundError as e:
            db.session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_admin()': {repr(e)}"
        except Exception as e:
            db.session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_admin()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(admin_result)
        finally:
            db.session.close()

        return {"status_code": status_code, "data": data}
