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
        # format: (*project_name, description)
        self.exist_project = 'exist_project'

        # Store all projects' name here
        self.project_list = None

        # name of sys_db of sqlite
        self.root_db_name = 'sqlite_master'

        # indicate the schema of project table
        self.project_tb_schema = None

        # indicate the schema of bill insertion
        self.bill_modify_schema = None

        # init db
        self.__init_db()

    def create_project(self):
        '''
        Abstract method
        '''
        raise NotImplementedError

    def delete_project(self, project_name: str):
        '''
        General:
            - delete a project with name: {project_name}
        Behavior:
            - If there's no such project -> ValueError()
            - else:
                - drop the table with project name {project_name}
                - delete a row from {self.exist_project} where project_name == project_name
                - remove the project from self.project_list
        '''

        project_name = project_name.lower()

        if project_name not in self.project_list:
            raise ValueError('project {} does not exist'.format(project_name))
            return

        # Drop the project table
        self._curr.execute('''DROP TABLE {} '''.format(project_name))

        # Delete the item from table exist_project
        sql = 'DELETE FROM {table_name} WHERE project_name=?'.format(
            table_name=self.exist_project)
        self._curr.execute(sql, (project_name,))

        # delete the projec from list
        self.project_list.remove(project_name)

        self._conn.commit()

    def update_project(self, old_tb_name: str, new_tb_name: str = None,
                       project_desc: str = None):
        '''
        General goal:
            - update a project
        Behavior:
            - If the project to be updated doesn't exist -> ValueError
            - If new_tb_name is provided: 
                - if the new_tb_name is not occupied, update the project name with new_tb_name. else -> ValueError
            - If project_desc is provided -> update the project description with project_desc
        '''

        if new_tb_name is None and project_desc is None:
            # there's nothing to update
            return

        # convert to lower case
        old_tb_name = old_tb_name.lower()

        if old_tb_name not in self.project_list:
            raise ValueError(
                'Table {name} not exist.'.format(name=old_tb_name))
            return

        if project_desc is not None:
            # update the project description
            self._curr.execute(
                '''UPDATE {tb_name} SET description={new_desc} where project_name={proj_name}'''.format(
                    tb_name=self.exist_project,
                    new_desc=project_desc.lower(),
                    proj_name=old_tb_name))

        if new_tb_name is not None:
            # Do modification on table name:
            new_tb_name = new_tb_name.lower()

            if new_tb_name in self.project_list:
                raise ValueError(
                    'Table {new_tb} already exist, choose a differnt name'.format(
                        new_tb=new_tb_name))
                return
            self._curr.execute(
                '''ALTER TABLE '{old}' RENAME TO '{new}' '''.format(
                    old=old_tb_name, new=new_tb_name))

            # update the project list:
            # replace the old one with the new one
            self.project_list.remove(old_tb_name)
            self.project_list.append(new_tb_name)

            # rename the project name in self.exist_project
            self._curr.execute(
                '''UPDATE {tb_name} SET project_name = '{new_name}' where project_name='{old_name}' '''.format(
                    tb_name=self.exist_project,
                    new_name=new_tb_name,
                    old_name=old_tb_name))

        self._conn.commit()

    def project_exist(self, project_name: str) -> bool:
        '''
        General goal:
            - Check whether the project already exist or not.
        '''

        if project_name in self.project_list:
            return True
        else:
            return False

    def insert_bills(self):
        '''
        Abstract method
        Insert bills into a specific table
        '''
        raise NotImplementedError

    def delete_bills(self):
        '''
        Abstract method
        Delete bills from a specific table
        '''
        raise NotImplementedError

    def update_bills(self):
        '''
        Abstract method
        Update bills in a specific table with new value
        '''
        raise NotImplementedError

    def list_items_in_table_with_name(self, table_name: str, max_num: int = None) -> list:
        '''
        General goal:
            - This method list items in specified table in a DB.
        Params:
            - table_name(str): indicate the target db table.
            - max_num: indicate how many items will be listed
        '''

        table_name = table_name.lower()

        table_result = self._curr.execute(
            '''SELECT * FROM {table_name}'''.format(table_name=table_name))

        if max_num is None:
            result = table_result.fetchall()
        else:
            result = table_result.fetchmany(max_num)

        return result

    def project_info(self, project_name: str) -> tuple:
        '''
        General goal:
            - List the project info from Table {exist_table}
        Return format:
            - (project_name, project_description)
        '''

        # get target project name
        project_name = project_name.lower()

        # if project doesn't exist
        if project_name not in self.project_list:
            raise ValueError(
                'Project {name} doesn\'t exist'.format(name=project_name))
            return

        # get the target project info
        msg = self._curr.execute(
            '''SELECT * FROM {table} WHERE project_name='{proj_name}' '''.format(
                table=self.exist_project, proj_name=project_name))

        return msg.fetchall()

    def __init_db(self):
        '''
        General goal:
            - Init the database
        '''

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
        result = self.list_items_in_table_with_name(
            self.exist_project)

        # format for each item: (project_name: str, description: str)
        self.project_list = [item[0] for item in result]


class GeneralProjectDAO(DAO):
    def __init__(self):
        super().__init__()

        # used in create a new General Project
        self.project_tb_schema = '''bill_index INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    title STRING NOT NULL,
                                    note STRING,
                                    time STRING NOT NULL,
                                    amount FLOAT NOT NULL'''

        self.bill_modify_schema = 'title,note,time,amount'

    def create_project(self, project_name: str, proj_desc: str):
        '''
        General:
            - Create a table with name: project_name, and project description: proj_desc.
        Behavior:
            - If the project with name {project_name} already exist -> ValueError

            - otherwise:
                - Create a new table with name {project_name}, schema: {self.project_tb_schema}.
                - Add a new item into table {self.project_exist}, with value (project_name, proj_desc).
                - Add the new table name into self.project_list.
        '''

        project_name = project_name.lower()
        proj_desc = proj_desc.lower()

        # Try to create a project here:
        if project_name in self.project_list:
            # If project already exist, raise a ValueError and return
            raise ValueError(
                '{project_name} already exist!'.format(
                    project_name=project_name))
            return

        print('Creating a General Project with name: {name}'.format(
            name=project_name))

        # Create the new table here:
        self._curr.execute('''CREATE TABLE {table_name} ({schema})'''.format(
            table_name=project_name, schema=self.project_tb_schema))

        # Add created table name into the self.project_list here:
        self.project_list.append(project_name)

        # Update self.exist_table here:
        self._curr.execute(
            '''INSERT INTO {table_name} (project_name, description) VALUES ('{proj_name}', '{proj_desc}')'''.format(
                table_name=self.exist_project,
                proj_name=project_name,
                proj_desc=proj_desc))

        # save changes
        self._conn.commit()

    def insert_bills(self, table_name: str, bills):
        '''
        Insert bills into table with name {table_name}, the bill_index is set to autoincrement.

        bills: iterable[Bill]
        '''

        if not bills:
            # bills is empty, just return
            return

        table_name = table_name.lower()
        # get the index of last bill and store it into index
        if table_name not in self.project_list:
            raise ValueError(
                '{project_name} doesn\'t exist!'.format(
                    project_name=table_name))
            return

        # insert bills into table:
        for item in bills:
            item = str(item)

            self._curr.execute(
                '''INSERT INTO {table_name} ({schema}) VALUES {item}'''.format(
                    table_name=table_name, schema=self.bill_modify_schema, item=item))

        self._conn.commit()
        print('Successful insert {count} bills.'.format(count=len(bills)))

    def delete_bills(self, table_name: str, bill_index):
        '''
        delete bills from specified table
        - params:
            - table_name : indicates target table
            - bill_index: iterable : a iterable object with bill index in it.
        '''
        table_name = table_name.lower()

        if table_name not in self.project_list:
            raise ValueError(
                '{project_name} doesn\'t exist!'.format(
                    project_name=table_name))
            return

        for index in bill_index:
            self._curr.execute(
                '''DELETE from {table_name} where bill_index={id}'''.format(
                    table_name=table_name, id=index))

        self._conn.commit()
        print('Successful delect {count} bills.'.format(count=len(bill_index)))

    def update_bills(self, table_name: str, bills):
        '''
        general:
            - update all bill in bills for target project {table_name}
        args:
            - bills: list[bill]
            - table_name: str, target project table name.
        '''

        table_name = table_name.lower()

        if table_name not in self.project_list:
            raise ValueError(
                '{project_name} doesn\'t exist!'.format(
                    project_name=table_name))
            return

        for bill in bills:
            sql = '''UPDATE {tb_name} SET 
                    title='{bill.title}', 
                    note='{bill.note}',
                    time='{bill.time}', 
                    amount={bill.amount} 
                    where bill_index = {bill.bill_index}'''.format(tb_name=table_name,
                                                                   bill=bill)
            self._curr.execute(sql)

        self._conn.commit()

        print('Successfully updated', len(bills), 'bill.')


if __name__ == '__main__':
    data_accessor = GeneralProjectDAO()

    try:
        data_accessor.create_project('hello', 'this is a test stirng')
    except ValueError:
        pass

    # For temp testing:
    import model

    data = [
        model.Bill(0, 'bill1', 'this is note for bill1', '2020/3/8', 100),
        model.Bill(1, 'bill2', 'this is note for bill2', '2020/3/8', -100),
        model.Bill(2, 'walsdf3', 'this is note for bill3', '2020/3/8', 101230)
    ]

    # data_accessor.insert_bills('hello', data)
    data_accessor.update_bills('hello', [data[2]])

    # data_accessor.delete_bills('hello', [0,1,2])
