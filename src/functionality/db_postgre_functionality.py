from src.lib.model import Admin, Organization, SuperAdmin, Queue, QueueUser, User
from typing import List


class DBPostgreFunctionality:
    """Handle DB connection & operation to antriin DB"""

    def __init__(self) -> None:
        pass

    def get_super_admin_using_email(self, super_admin_email: str) -> SuperAdmin:
        """get super admin data using email"""

        return SuperAdmin.query.filter_by(email=super_admin_email).first()

    def get_super_admin_using_super_admin_id(self, super_admin_id: int) -> dict:

        return SuperAdmin.query.filter_by(id=super_admin_id).first()

    def get_org_using_super_admin_id(self, super_admin_id: int) -> Organization:
        """get organization data using super admin id"""

        return Organization.query.filter_by(super_admin_id=super_admin_id).first()

    def get_admin_using_admin_email(self, admin_email: str) -> Admin:

        return Admin.query.filter_by(email=admin_email).first()

    def get_admin_using_org_id(self, org_id: str) -> List[Admin]:
        """get admin data using organization id"""

        return Admin.query.filter_by(organization_id=org_id).all()

    def get_admin_using_org_id_and_admin_id(self, org_id: str, admin_id: int) -> Admin:
        """get admin data using organization id and admin id"""

        return Admin.query.filter_by(organization_id=org_id, id=admin_id).first()

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

    def get_queue_using_queue_id(self, queue_id: int) -> Queue:

        return Queue.query.filter_by(id=queue_id).first()

    def get_queue_using_list_queue_user(self, list_queue_user: list) -> Queue:

        return Queue.query.filter(
            Queue.id.in_([queue_user.queue_id for queue_user in list_queue_user])
        ).all()

    def get_queue_using_list_queue_user_and_queue_id(
        self, list_queue_user: list, queue_id: int
    ) -> Queue:

        return Queue.query.filter(
            Queue.id.in_([queue_user.queue_id for queue_user in list_queue_user]),
            Queue.id == queue_id,
        ).first()

    def get_queue_using_admin_id(self, admin_id: int) -> List[Queue]:

        return Queue.query.filter_by(admin_id=admin_id).all()

    def get_queue_using_admin_id_and_queue_id(
        self, queue_id: int, admin_id: int
    ) -> Queue:

        return Queue.query.filter_by(admin_id=admin_id, id=queue_id).first()

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

    def get_queue_in_list_by_admin(self, queue_id: int, admin_id: int) -> list:

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

    def get_user_using_user_id(self, user_id: int) -> User:

        return User.query.filter_by(id=user_id).first()

    def get_user_using_user_email(self, user_email: str) -> User:

        return User.query.filter_by(email=user_email).first()

    def get_user_using_queue_user(self, queue_user_result: list) -> List[User]:

        return User.query.filter(
            User.id.in_([queue_user.user_id for queue_user in queue_user_result])
        ).all()

    def get_user_using_queue_user_and_user_id(
        self, queue_user_result: list, user_id: int
    ) -> User:

        return User.query.filter(
            User.id.in_([queue_user.user_id for queue_user in queue_user_result]),
            User.id == user_id,
        ).first()

    def get_user_in_list(self, queue_user_list: list, user_id: int) -> list:

        user_result = (
            self.get_user_using_queue_user_and_user_id(queue_user_list, user_id)
            if user_id
            else self.get_user_using_queue_user(queue_user_list)
        )

        # convert query result to list
        user_list = []
        if user_result:
            if isinstance(user_result, list):
                user_list = user_list + user_result
            else:
                user_list.append(user_result)

        return user_list

    def get_queue_user_using_user_id(self, user_id: int) -> QueueUser:

        return QueueUser.query.filter_by(user_id=user_id).all()

    def get_queue_user_using_list_queue(self, list_queue: list) -> QueueUser:

        return QueueUser.query.filter(
            QueueUser.queue_id.in_([queue.id for queue in list_queue])
        ).all()

    def get_queue_user_using_queue_id_and_user_id(
        self, queue_id: int, user_id: int
    ) -> QueueUser:

        return QueueUser.query.filter_by(queue_id=queue_id, user_id=user_id).first()

    def get_queue_user_using_list_queue_and_queue_user_id(
        self, list_queue: list, queue_user_id: int
    ) -> QueueUser:

        return QueueUser.query.filter(
            QueueUser.queue_id.in_([queue.id for queue in list_queue]),
            QueueUser.id == queue_user_id,
        ).first()

    def get_queue_user_in_list(
        self, list_queue: list, queue_user_id: int
    ) -> List[QueueUser]:

        queue_user_result = (
            self.get_queue_user_using_list_queue_and_queue_user_id(
                list_queue, queue_user_id
            )
            if queue_user_id
            else self.get_queue_user_using_list_queue(list_queue)
        )

        # convert query result to list
        queue_user_list = []
        if queue_user_result:
            if isinstance(queue_user_result, list):
                queue_user_list = queue_user_list + queue_user_result
            else:
                queue_user_list.append(queue_user_result)

        return queue_user_list
