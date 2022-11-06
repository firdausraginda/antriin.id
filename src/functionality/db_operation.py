from src.lib.model import Admin, Organization, SuperAdmin, Queue, QueueUser, User, db

class DBOperation:
    """Handle DB connection & operation to antriin DB"""

    def __init__(self) -> None:
        pass

    def get_element(self, query_result, is_get_one_element: bool):
        """to determine get all elements or only 1 element from query result"""

        return query_result.first() if is_get_one_element is True else query_result.all()

    def get_super_admin_using_email(self, super_admin_email: str, is_get_one_element: bool):
        """get super admin data using email"""
        
        query_result = SuperAdmin.query.filter_by(email=super_admin_email)
        
        return self.get_element(query_result, is_get_one_element)

    def get_super_admin_using_super_admin_id(self, super_admin_id: str, is_get_one_element: bool):

        query_result = SuperAdmin.query.filter_by(id=super_admin_id)

        return self.get_element(query_result, is_get_one_element)

    def get_org_using_super_admin_id(self, super_admin_id: str, is_get_one_element: bool):
        """get organization data using super admin id"""

        query_result = Organization.query.filter_by(super_admin_id=super_admin_id).first()

        return self.get_element(query_result, is_get_one_element)

    def get_admin_using_org_id(self, org_id: str, admin_id: str, is_get_one_element: bool):
        """get admin data using organization id"""

        filters = (Admin.organization_id == org_id,)
        if id:
            filters = filters + ((Admin.id == admin_id),)
        
        query_result = Admin.query.filter(*filters)

        return self.get_element(query_result, is_get_one_element)
    
    def get_org_using_super_admin_id(self, super_admin_id: str, org_id: str, is_get_one_element: bool):

        filters = (Organization.super_admin_id == super_admin_id,)
        if id:
            filters = filters + ((Organization.id == org_id),)
        
        query_result = Organization.query.filter(*filters)

        return self.get_element(query_result, is_get_one_element)

    def get_admin_using_admin_email(self, admin_email: str, is_get_one_element: bool):
        
        query_result = Admin.query.filter_by(email=admin_email)

        return self.get_element(query_result, is_get_one_element)

    def get_queue_using_admin_id(self, admin_id: str, queue_id: str, is_get_one_element: bool):

        filters = (Queue.admin_id == admin_id,)
        if id:
            filters = filters + ((Queue.id == queue_id),)
        
        query_result = Queue.query.filter(*filters)

        return self.get_element(query_result, is_get_one_element)

    def get_queue_user_using_queue_user_id(self, list_queue: list, queue_user_id: str, is_get_one_element: bool):

        filters = (QueueUser.queue_id.in_([queue.id for queue in list_queue]),)
        if id:
            filters = filters + ((QueueUser.id == queue_user_id),)
        
        query_result = QueueUser.query.filter(*filters)

        return self.get_element(query_result, is_get_one_element)

    def get_queue_using_queue_id(self, queue_id: str, is_get_one_element: bool):

        query_result = Queue.query.filter_by(id=queue_id)

        return self.get_element(query_result, is_get_one_element)

    def get_user_using_user_id(self, user_id: str, is_get_one_element: bool):

        query_result = User.query.filter_by(id=user_id)

        return self.get_element(query_result, is_get_one_element)

    def get_user_using_user_email(self, user_email: str, is_get_one_element: bool):

        query_result = User.query.filter_by(id=user_email)

        return self.get_element(query_result, is_get_one_element)

    def get_queue_user_using_queue_id_and_user_id(self, queue_id: str, user_id: str, is_get_one_element: bool):

        query_result = QueueUser.query.filter_by(queue_id=queue_id,user_id=user_id)

        return self.get_element(query_result, is_get_one_element)
    
    def get_queue_user_using_user_id(self, user_id: str, is_get_one_element: bool):

        query_result = QueueUser.query.filter_by(user_id=user_id)

        return self.get_element(query_result, is_get_one_element)

    def get_queue_user_using_list_queue_and_queue_user_id(self, list_queue: list, queue_user_id: str, is_get_one_element: bool):

        query_result = QueueUser.query.filter(QueueUser.queue_id.in_([queue.id for queue in list_queue]),QueueUser.id==queue_user_id)

        return self.get_element(query_result, is_get_one_element)

    def get_queue_using_list_queue_user(self, list_queue_user: list, is_get_one_element: bool):

        query_result = Queue.query.filter(Queue.id.in_([queue_user.queue_id for queue_user in list_queue_user]))

        return self.get_element(query_result, is_get_one_element)