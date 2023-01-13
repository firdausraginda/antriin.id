from src.functionality.db_postgre_functionality import DBPostgreFunctionality
from src.lib.model_v2 import Organization
from src.lib.custom_exception import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.lib.custom_exception import NotFoundError
from sqlalchemy.exc import IntegrityError
from src.lib.function import convert_model_to_dict, update_existing_data
from sqlmodel import Session


class OrganizationUsecase:
    def __init__(self, db_postgre_functionality: DBPostgreFunctionality) -> None:
        self._db_postgre_functionality = db_postgre_functionality

    def get_organization(self, super_admin_email: str) -> dict:
        """get organization data per super_admin_email"""

        session = self._db_postgre_functionality.start_session()

        super_admin_result = session.exec(
            self._db_postgre_functionality.get_super_admin_using_email(
                super_admin_email
            )
        ).first()

        org_result = session.exec(
            self._db_postgre_functionality.get_org_using_super_admin_id(
                super_admin_result.id
            )
        ).first()

        try:
            if not org_result:
                raise NotFoundError()
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'get_organization()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'get_organization()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(org_result)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def post_organization(self, super_admin_email: str, body_data: dict) -> dict:
        """insert organization data"""

        session = self._db_postgre_functionality.start_session()

        super_admin_result = session.exec(
            self._db_postgre_functionality.get_super_admin_using_email(
                super_admin_email
            )
        ).first()

        organization = Organization.validate(
            {
                "name": body_data.get("name"),
                "description": body_data.get("description"),
                "super_admin_id": super_admin_result.id,
            }
        )

        try:
            session.add(organization)
            session.commit()
            session.refresh(organization)
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'post_organization()': {repr(e)}"
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'post_organization()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'post_organization()': {repr(e)}"
        else:
            status_code = HTTP_201_CREATED
            data = convert_model_to_dict(organization)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def delete_organization(self, super_admin_email: str) -> dict:
        """delete organization data using super_admin_email"""

        session = self._db_postgre_functionality.start_session()

        super_admin_result = session.exec(
            self._db_postgre_functionality.get_super_admin_using_email(
                super_admin_email
            )
        ).first()

        org_result = session.exec(
            self._db_postgre_functionality.get_org_using_super_admin_id(
                super_admin_result.id
            )
        ).first()

        try:
            if not org_result:
                raise NotFoundError()

            session.delete(org_result)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'delete_organization()': {repr(e)}"
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'delete_organization()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'delete_organization()': {repr(e)}"
        else:
            status_code = HTTP_204_NO_CONTENT
            data = None  # if deletion success, didn't return any result
        finally:
            session.close()

        return {"status_code": status_code, "data": data}

    def edit_organization(self, super_admin_email: str, body_data: dict) -> dict:
        """edit organization data using super_admin_email"""

        session = self._db_postgre_functionality.start_session()

        super_admin_result = session.exec(
            self._db_postgre_functionality.get_super_admin_using_email(
                super_admin_email
            )
        ).first()

        org_result = session.exec(
            self._db_postgre_functionality.get_org_using_super_admin_id(
                super_admin_result.id
            )
        ).first()

        try:
            if not org_result:
                raise NotFoundError()

            # update existing organization with updated data
            update_existing_data(org_result, body_data)

            # validate updated organization
            Organization.validate({**convert_model_to_dict(org_result)})

            session.add(org_result)
            session.commit()
            session.refresh(org_result)
        except IntegrityError as e:
            session.rollback()
            status_code = HTTP_400_BAD_REQUEST
            data = f"Error in function 'edit_organization()': {repr(e)}"
        except NotFoundError as e:
            session.rollback()
            status_code = HTTP_404_NOT_FOUND
            data = f"Error in function 'edit_organization()': {repr(e)}"
        except Exception as e:
            session.rollback()
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            data = f"Error in function 'edit_organization()': {repr(e)}"
        else:
            status_code = HTTP_200_OK
            data = convert_model_to_dict(org_result)
        finally:
            session.close()

        return {"status_code": status_code, "data": data}
