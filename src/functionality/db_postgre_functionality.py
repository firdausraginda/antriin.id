from src.lib.model import Admin, Organization, SuperAdmin, Queue, QueueUser, User
from typing import List


class DBPostgreFunctionality:
    """Handle DB connection & operation to antriin DB"""

    def __init__(self) -> None:
        pass

    def get_super_admin_using_email(self, super_admin_email: str) -> SuperAdmin:
        """get super admin data using email"""

        query_result = SuperAdmin.query.filter_by(email=super_admin_email).first()

        return query_result

    def get_super_admin_using_super_admin_id(self, super_admin_id: int) -> dict:

        query_result = SuperAdmin.query.filter_by(id=super_admin_id).first()

        return query_result

    def get_org_using_super_admin_id(self, super_admin_id: int) -> Organization:
        """get organization data using super admin id"""

        query_result = Organization.query.filter_by(
            super_admin_id=super_admin_id
        ).first()

        return query_result

    def get_admin_using_admin_email(self, admin_email: str) -> Admin:

        query_result = Admin.query.filter_by(email=admin_email).first()

        return query_result

    def get_admin_using_org_id(self, org_id: str) -> List[Admin]:
        """get admin data using organization id"""

        query_result = Admin.query.filter_by(organization_id=org_id).all()

        return query_result

    def get_admin_using_org_id_and_admin_id(self, org_id: str, admin_id: int) -> Admin:
        """get admin data using organization id and admin id"""

        query_result = Admin.query.filter_by(
            organization_id=org_id, id=admin_id
        ).first()

        return query_result

    def get_admin_in_list(self, org_id: str, admin_id: int) -> list:

        admin_result = (
            self.get_admin_using_org_id_and_admin_id(org_id, admin_id)
            if admin_id
            else self.get_admin_using_org_id(org_id)
        )

        # convert query result to list
        admin_list = []
        if admin_result:
            if isinstance(admin_result, list):
                admin_list = admin_list + admin_result
            else:
                admin_list.append(admin_result)

        return admin_list

    def get_queue_using_admin_id(self, admin_id: int) -> List[Queue]:

        query_result = Queue.query.filter_by(admin_id=admin_id).all()

        return query_result

    def get_queue_using_admin_id_and_queue_id(
        self, queue_id: int, admin_id: int
    ) -> Queue:

        query_result = Queue.query.filter_by(admin_id=admin_id, id=queue_id).first()

        return query_result

    def get_queue_in_list(self, queue_id: int, admin_id: int) -> list:

        queue_result = (
            self.get_queue_using_admin_id_and_queue_id(queue_id, admin_id)
            if queue_id
            else self.get_queue_using_admin_id(admin_id)
        )

        # convert query result to list
        queue_list = []
        if queue_result:
            if isinstance(queue_result, list):
                queue_list = queue_list + queue_result
            else:
                queue_list.append(queue_result)

        return queue_list

    def get_queue_user_using_queue_user_id(
        self, list_queue: list, queue_user_id: int
    ) -> QueueUser:

        filters = (QueueUser.queue_id.in_([queue.id for queue in list_queue]),)
        if id:
            filters = filters + ((QueueUser.id == queue_user_id),)

        query_result = QueueUser.query.filter(*filters).first()

        return query_result

    def get_queue_using_queue_id(self, queue_id: int) -> Queue:

        query_result = Queue.query.filter_by(id=queue_id).first()

        return query_result

    def get_user_using_user_id(self, user_id: int) -> User:

        query_result = User.query.filter_by(id=user_id).first()

        return query_result

    def get_user_using_user_email(self, user_email: str) -> User:

        query_result = User.query.filter_by(email=user_email).first()

        return query_result

    def get_queue_user_using_queue_id_and_user_id(
        self, queue_id: int, user_id: int
    ) -> QueueUser:

        query_result = QueueUser.query.filter_by(
            queue_id=queue_id, user_id=user_id
        ).first()

        return query_result

    def get_queue_user_using_user_id(self, user_id: int) -> QueueUser:

        query_result = QueueUser.query.filter_by(user_id=user_id).all()

        return query_result

    def get_queue_user_using_list_queue_and_queue_user_id(
        self, list_queue: list, queue_user_id: int
    ) -> QueueUser:

        query_result = QueueUser.query.filter(
            QueueUser.queue_id.in_([queue.id for queue in list_queue]),
            QueueUser.id == queue_user_id,
        ).first()

        return query_result

    def get_queue_using_list_queue_user(self, list_queue_user: list) -> Queue:

        query_result = Queue.query.filter(
            Queue.id.in_([queue_user.queue_id for queue_user in list_queue_user])
        ).all()

        return query_result

    def get_queue_using_list_queue_user_and_queue_id(
        self, list_queue_user: list, queue_id: int
    ) -> Queue:

        query_result = Queue.query.filter(
            Queue.id.in_([queue_user.queue_id for queue_user in list_queue_user]),
            Queue.id == queue_id,
        ).first()

        return query_result

    def get_queue_in_list_by_user(self, list_queue_user: list, queue_id: int):

        queue_result = (
            self.get_queue_using_list_queue_user_and_queue_id(list_queue_user, queue_id)
            if queue_id
            else self.get_queue_using_list_queue_user(list_queue_user)
        )

        # convert query result to list
        queue_list = []
        if queue_result:
            if isinstance(queue_result, list):
                queue_list = queue_list + queue_result
            else:
                queue_list.append(queue_result)

        return queue_list
