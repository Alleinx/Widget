import sqlite3

class DAO(object):
    '''
    Data Access Object
    '''

    def __init__(self):
        self._conn = sqlite3.connect('data/pbank.db')
        self._curr = self._conn.cursor()
        self.project_list = []

        # init db
        self._init_db()

    def create_table(self, project):
        raise NotImplementedError

    def delete_table(self, project_name: str):
        '''
        delete table related to project
        '''
        raise NotImplementedError

    def project_exist(self, project_name: str) -> bool:
        if project_name in self.project_list:
            return True
        else:
            return False

    def save(self, project):
        '''
        save changes of project
        '''
        raise NotImplementedError

    def _init_db(self):
        print('Init')
        pass
        # raise NotImplementedError

class GeneralProjectDAO(DAO):
    pass
