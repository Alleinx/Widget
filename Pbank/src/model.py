class Project(object):
    '''
    Model class, project
    '''

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._bills = []

    def add_bill(bill):
        raise NotImplementedError

    def update_bill(bill):
        raise NotImplementedError

    def delete_bill(bill):
        raise NotImplementedError


class ProjectFactory(object):
    '''
    Project Factory
    '''

    def __init__(self, data_accessor):
        self.data_accessor = data_accessor

    def fetch_project(self, project_name: str) -> Project:
        '''
        This method tends to build and return a Project with project_name
        '''
        pass

    def create_project(self):
        '''
        This method tends to create a new project
        '''
        pass
