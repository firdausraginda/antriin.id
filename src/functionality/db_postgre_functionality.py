from src.lib.model_v2 import Admin, Organization, Queue, QueueUser, User
from sqlmodel import Session
from sqlmodel import select, col


class DBPostgreFunctionality:
    """Handle DB connection & operation to antriin DB"""

    def __init__(self, engine) -> None:
        self._engine = engine

    def start_session(self):
        """initiate session to database"""

        return Session(self._engine)

    def get_org_using_admin_id(self, admin_id: int) -> Organization:
        """get organization data using admin id"""

        return select(Organization).where(Organization.admin_id == admin_id)

    def get_org_using_super_admin_id(self, super_admin_id: int) -> Organization:
        """get organization data using super admin id"""

        return select(Organization).where(Organization.super_admin_id == super_admin_id)

    def get_admin_using_admin_email(self, admin_email: str) -> Admin:
        """get admin using admin_email"""

        return select(Admin).where(Admin.email == admin_email)

    def get_admin_using_org_id(self, org_id: str) -> Admin:
        """get admin data using organization id"""

        return select(Admin).where(Admin.organization_id == org_id)

    def get_admin_using_org_id_and_admin_id(self, org_id: str, admin_id: int) -> Admin:
        """get admin data using organization id and admin id"""

        return select(Admin).where(
            Admin.organization_id == org_id, Admin.id == admin_id
        )

    def get_admin_in_list(self, org_id: str, admin_id: int) -> Admin:
        """get list of admin using organization_id and admin_id if any"""

        return (
            self.get_admin_using_org_id_and_admin_id(org_id, admin_id)
            if admin_id
            else self.get_admin_using_org_id(org_id)
        )

    def get_queue_using_queue_id(self, queue_id: int) -> Queue:
        """get queue using queue_id"""

        return select(Queue).where(Queue.id == queue_id)

    def get_queue_using_list_queue_user(self, list_queue_user: list) -> Queue:
        """get queue using list of queue user"""

        return select(Queue).where(
            col(Queue.id).in_([queue_user.queue_id for queue_user in list_queue_user])
        )

    def get_queue_using_list_queue_user_and_queue_id(
        self, list_queue_user: list, queue_id: int
    ) -> Queue:
        """get queue using list of queue user and queue_id"""

        return select(Queue).where(
            col(Queue.id).in_([queue_user.queue_id for queue_user in list_queue_user]),
            Queue.id == queue_id,
        )

    def get_queue_using_admin_id(self, admin_id: int) -> Queue:
        """get queue using admin_id"""

        return select(Queue).where(Queue.admin_id == admin_id)

    # def get_queue_using_user_id(self, user_id: int) -> Queue:
    #     """get queue using user_id"""

    #     return select(Queue).where(Queue.user_id == user_id)

    def get_queue_using_short_url(self, short_url: str) -> Queue:
        """get queue using short_url"""

        return select(Queue).where(Queue.short_url == short_url)

    def get_queue_using_admin_id_and_queue_id(
        self, queue_id: int, admin_id: int
    ) -> Queue:
        """get queue using admin_id and queue_id"""

        return select(Queue).where(Queue.admin_id == admin_id, Queue.id == queue_id)

    def get_queue_in_list_by_user(self, list_queue_user: list, queue_id: int) -> Queue:
        """get list of queue using list of queue user and queue_id if any"""

        return (
            self.get_queue_using_list_queue_user_and_queue_id(list_queue_user, queue_id)
            if queue_id
            else self.get_queue_using_list_queue_user(list_queue_user)
        )

    def get_queue_in_list_by_admin(self, queue_id: int, admin_id: int) -> Queue:
        """get list of queue using admin_id and queue_id if any"""

        return (
            self.get_queue_using_admin_id_and_queue_id(queue_id, admin_id)
            if queue_id
            else self.get_queue_using_admin_id(admin_id)
        )

    def get_user_using_user_id(self, user_id: int) -> User:
        """get user using user_id"""

        return select(User).where(User.id == user_id)

    def get_user_using_user_email(self, user_email: str) -> User:
        """get user using user_email"""

        return select(User).where(User.email == user_email)

    def get_user_using_queue_user(self, queue_user_result: list) -> User:
        """get user using list of queue user"""

        return select(User).where(
            col(User.id).in_([queue_user.user_id for queue_user in queue_user_result])
        )

    def get_user_using_queue_user_and_user_id(
        self, queue_user_result: list, user_id: int
    ) -> User:
        """get user using list of queue user and user_id"""

        return select(User).where(
            col(User.id).in_([queue_user.user_id for queue_user in queue_user_result]),
            User.id == user_id,
        )

    def get_user_in_list(self, queue_user_list: list, user_id: int) -> User:
        """get list of users using list of queue user and user_id if any"""

        return (
            self.get_user_using_queue_user_and_user_id(queue_user_list, user_id)
            if user_id
            else self.get_user_using_queue_user(queue_user_list)
        )

    def get_queue_user_using_user_id(self, user_id: int) -> QueueUser:
        """get queue user using user_id"""

        return select(QueueUser).where(QueueUser.user_id == user_id)

    def get_queue_and_user_info_using_user_id(self, user_id: int) -> Queue:
        """get queue using list of queue_user"""

        return (
            select(
                Queue.id,
                Queue.name,
                Queue.current_queue_number,
                Queue.total_queue_number,
                QueueUser.queue_number,
            )
            .join(QueueUser, isouter=True)
            .join(User, isouter=True)
            .where(User.id == user_id)
        )

    def get_queue_and_user_info_using_user_id_and_queue_id(
        self, user_id: int, queue_id: int
    ) -> Queue:
        """get queue using list of queue_user"""

        return (
            select(
                Queue.id,
                Queue.name,
                Queue.current_queue_number,
                Queue.total_queue_number,
                QueueUser.queue_number,
            )
            .join(QueueUser, isouter=True)
            .join(User, isouter=True)
            .where(User.id == user_id, Queue.id == queue_id)
        )

    def get_queue_and_user_info_in_list(self, user_id: int, queue_id: int) -> Queue:
        """get queue info using list queue_user and queue_id if any"""

        return (
            self.get_queue_and_user_info_using_user_id_and_queue_id(user_id, queue_id)
            if queue_id
            else self.get_queue_and_user_info_using_user_id(user_id)
        )

    def get_queue_user_using_list_queue(self, list_queue: list) -> QueueUser:
        """get queue user using list of queue"""

        return select(QueueUser).where(
            col(QueueUser.queue_id).in_([queue.id for queue in list_queue])
        )

    def get_queue_user_using_queue_id_and_user_id(
        self, queue_id: int, user_id: int
    ) -> QueueUser:
        """get queue user using queue_id and user_id"""

        return select(QueueUser).where(
            QueueUser.queue_id == queue_id, QueueUser.user_id == user_id
        )

    def get_queue_user_using_list_queue_and_queue_user_id(
        self, list_queue: list, queue_user_id: int
    ) -> QueueUser:
        """get queue user using list of queue and queue_user_id"""

        return select(QueueUser).where(
            col(QueueUser.queue_id).in_([queue.id for queue in list_queue]),
            QueueUser.id == queue_user_id,
        )

    def get_queue_user_in_list(self, list_queue: list, queue_user_id: int) -> QueueUser:
        """get queue user using list of queue and queue_user_id if any"""

        return (
            self.get_queue_user_using_list_queue_and_queue_user_id(
                list_queue, queue_user_id
            )
            if queue_user_id
            else self.get_queue_user_using_list_queue(list_queue)
        )
