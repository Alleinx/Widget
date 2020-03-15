import data_util as dao


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

    def get_all_bills(self) -> list:
        return self._bills

    def __repr__(self):
        return f'(Project: {self.name}; Project description: {self.description})'

    def __str__(self):
        return f'{self.name}'


class GeneralProject(Project):

    def __init__(self, name: str, description: str):
        super().__init__(name, description)

    def add_bill(self, bill):
        bill = Bill(*bill)
        self._bills.append(bill)

    def update_bill(self, old_bill, new_bill):
        pass

    def delete_bill(self, bill):
        pass


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

    def __str__(self):
        return '(\'{self.title}\', \'{self.note}\', \'{self.time}\', {self.amount})'.format(self=self)

    def __repr__(self):
        return f'({self.time}: Bill[{self.bill_index}] <Title>: {self.title}, <Amount>: {self.amount}, <Note>: {self.note})'

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


class ProjectAbstractFactory(object):
    '''
    abc class, used to define a general interface for ProjectFactory
    '''

    def __init__(self, dao):
        self.data_accessor = dao
        self.project_list = None
        self._init()

    def fetch_project(self):
        raise NotImplementedError

    def create_project(self):
        raise NotImplementedError

    def delete_project(self):
        raise NotImplementedError

    def update_project(self):
        raise NotImplementedError

    def _init(self):
        raise NotImplementedError



class GeneralProjectFactory(ProjectAbstractFactory):
    '''
    Project Factory
    '''

    def __init__(self):
        super().__init__(dao.GeneralProjectDAO())

    def _init(self):
        self.project_list = dict()

        for project in self.data_accessor.project_list:
            project_description = self.data_accessor.get_project_description(
                project)

            new_project = GeneralProject(project, project_description)

            project_bill = self.data_accessor.get_project_bill(project)
            for item in project_bill:
                new_project.add_bill(item)

            self.project_list[new_project.name] = new_project

    def fetch_project(self, project_name: str) -> Project:
        '''
        This method tends to build and return a Project with project_name
        '''
        if project_name not in self.project_list:
            return ValueError(
                'Project {} doesn\'t exist.'.format(project_name))
        else:
            '''
            fetch data from data_accessor
                and build the Project object.
            '''
            return self.project_list[project_name]

    def create_project(self, project_name: str,
                       description='Project Description') -> Project:
        '''
        This method tends to create a new project
        '''
        if project_name in self.project_list:
            raise ValueError('Project {} already exist.'.format(project_name))
        else:
            project = Project(project_name, description)
            self.project_list[project_name] = project
            self.data_accessor.create_project(project_name, description)
            return project
    
    def display_project_info(self) -> list:
        """For Menu Displaying
        
        Returns:
            list -- a list contains all project in the db.
        """

        return [item for item in self.project_list.values()]


if __name__ == "__main__":
    project_manager = GeneralProjectFactory()
    name = 'hello'
    print(project_manager.project_list)
    project = project_manager.project_list[name]
    print(project.name)
    print(project._bills)