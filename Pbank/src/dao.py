import sqlite3

class DAO(object):
    '''
    Data Access Object
    '''

    def __init__(self):
        self.conn = sqlite3.connect('data/pbank.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        pass

