import sqlite3


class DAO(object):
    '''
    Data Access Object
    '''

    def __init__(self):
        self._conn = sqlite3.connect('data/pbank.db')

        # DB cursor:
        self._curr = self._conn.cursor()

        # DB table name for exist_project, which stores all projects'
        # description.
        # format: (*project_name, project_description)
        self.exist_project = 'exist_project'

        # Store all projects' name here
        self.project_list = None

        # name of sys_db of sqlite
        self.root_db_name = 'sqlite_master'

        # init db
        self.__init_db()

    def create_table(self):
        raise NotImplementedError

    def delete_table(self):
        raise NotImplementedError

    def project_exist(self, project_name: str) -> bool:
        if project_name in self.project_list:
            return True
        else:
            return False

    def insert_items(self):
        '''
        Insert items into a specific table
        '''
        raise NotImplementedError

    def delete_items(self):
        '''
        Delete items from a specific table
        '''
        raise NotImplementedError

    def update_items(self):
        '''
        Update items in a specific table with new value
        '''
        raise NotImplementedError

    def accept(self, visitor):
        '''
        Store visitor for handling format of Bill.
        '''
        # TODO: may need to move to AbstractFactory/ProjectHandler class.

        self.visitor = visitor

    def list_items_in_table_with_name(self, table_name: str, max_num=None) -> list:
        '''
        This method list items in db table with name
        - Params:
            - table_name(str): indicate the target db table
            - max_num: indicate how many items will be listed
        '''

        table_result = self._curr.execute(
                            '''SELECT * FROM {table_name}'''.format(table_name=table_name))
        if not max_num:
            result = table_result.fetchall()
        else:
            result = table_result.fetchmany(max_num)

        return result

    def __init_db(self):
        print('Init databases')

        # Build the table for project description.
        try:
            print('Trying to creating exist_project Table.')
            self._curr.execute('''CREATE TABLE {self.exist_project}
                                (project_name TEXT PRIMARY KEY NOT NULL,
                                description TEXT)'''.format(self=self))
        except sqlite3.OperationalError:
            print('exist_project Table already exist.')

        # Store all items in exist_project TABLE into project_list
        self.project_list = self.list_items_in_table_with_name(self.exist_project)

        print(self.project_list)


class GeneralProjectDAO(DAO):
    def create_table(self, project_name: str, proj_desc: str, bill):
        '''
        - create 1 tables:
            - Table with project_name as name, and each row is formatted as bill.get_format()
        - Update 1 table:
            - TABLE with self.exist_table as name.
        - Add created table name into the self.project_list
        '''
        print('Creating a General Project.')

        # Create the table here:
        format = bill.get_format()
        format = self.visitor.visit(format)

        try:
            self._curr.execute('''CREATE TABLE {table_name}
                               ({format})'''.format(table_name=project_name, format=format))
        except sqlite3.OperationalError:
            print(
                '{project_name} already exist!'.format(
                    project_name=project_name))
            raise RuntimeError(
                '{project_name} already exist!'.format(
                    project_name=project_name))
            return

        # Update self.exist_table here:
        # TODO

        # Add created table name into the self.project_list here
        self.project_list.append(project_name)

    def insert_items(self, table_name: str, items: iterable[Bill]):
        # TODO: get the index of last bill and store it into index
        index = len(None)

        # insert items into table:
        for item in item:
            value = list(index)
            value.extend(item)

            value = tuple(value)
            index += 1
            self._curr.execute('''INSERT INTO {table_name} VALUES ({item})'''.format(table_name=table_name, item=value))

        self._conn.commit()

    def delete_items(self, table_name: str, bill_indexs: iterable):
        '''
        delete bills from specified table
        - params:
            - table_name : indicates target table
            - bill_index : a iterable object with bill index in it.
        '''
        for index in bill_index:
            self._curr.execute('''DELETE from {table_name} where ID={id}'''.format(table_name=table_name, id=index))

        self._conn.commit()

if __name__ == '__main__':
    data_accessor = GeneralProjectDAO()
    data_accessor.create_table('test')
