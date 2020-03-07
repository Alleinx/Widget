import data_util as dao


class ProjectAbstractFactory(object):
    '''
    abc class, used to define a general interface for ProjectFactory
    '''

    def __init__(self, dao):
        self.data_accessor = dao
        self.project_list = []

    def fetch_project(self):
        raise NotImplementedError

    def create_project(self):
        raise NotImplementedError


class Project(object):
    '''
    abc class, used to define a general interface for Project
    '''

    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description

        self._bills: list = []
        # use to store a snapshoot of data stored in db.

    def add_bill(self, bill):
        raise NotImplementedError

    def update_bill(self, old_bill, new_bill):
        raise NotImplementedError

    def delete_bill(self, bill):
        raise NotImplementedError


class Bill(object):
    '''
    Used to store transfer record
    '''

    def __init__(self, bill_index: int, title: str,
                 note: str, time: str, amount: float):

        self.bill_index = bill_index
        self.amount = amount
        self.time = time
        self.title = title
        self.note = note

    @property
    def bill_index(self):
        return self._bill_index

    @bill_index.setter
    def bill_index(self, value):
        if not isinstance(value, int):
            raise ValueError('bill index should be an integer')

        if value < 0:
            raise ValueError('bill index should >= 0')
        else:
            self._bill_index = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        '''
        If no title is provided, should not be created
        '''
        if not isinstance(title, str):
            raise ValueError('Title should be a str')

        if title is None:
            return ValueError('Bill must have a Title or tag')
        else:
            self._title = title

    def __str__(self):
        return '({self.bill_index}, \'{self.title}\', \'{self.note}\', \'{self.time}\', {self.amount})'.format(self=self)


class GeneralProject(Project):

    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    def add_bill(self, bill):
        self._bills.append(bill)

    def update_bill(self, old_bill, new_bill):
        pass

    def delete_bill(self, bill):
        pass


class GeneralProjectFactory(ProjectAbstractFactory):
    '''
    Project Factory
    '''

    def __init__(self):
        super().__init__(dao.GeneralProjectDAO())

    def fetch_project(self, project_name: str) -> Project:
        '''
        This method tends to build and return a Project with project_name
        '''
        if not self.data_accessor.project_exist(project_name):
            return ValueError(
                'Project {} doesn\'t exist.'.format(project_name))
        else:
            '''
            fetch data from data_accessor
                and build the Project object.
            '''
            raise NotImplementedError

    def create_project(self, project_name: str,
                       description='Project Description'):
        '''
        This method tends to create a new project
        '''
        if self.data_accessor.project_exist(project_name):
            raise ValueError('Project {} already exist.'.format(project_name))
        else:
            project = Project(project_name, description)
            return project
