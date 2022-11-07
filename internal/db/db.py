"""
This module is a MySQL connector with context manager
"""
import pymysql
from flask import current_app, g


def get_db(multi=False):
    if 'db' not in g:
        db_conf = current_app.config['DB_CONF']
        g.db = MySQL(
            host=db_conf['host'],
            user=db_conf['user'],
            password=db_conf['password'],
            database=db_conf['database'],
            port=db_conf['port'],
            multi=multi,
        )
    return g.db


class MySQL(object):
    """
    MySQL connection context manager
    """

    def __init__(self, host, port, user, password, database, timeout=60, multi=False):
        self.conn = None
        self.cursor = None
        """
        Enter the runtime context
        Return a dictionary cursor
        Retry 3 times when connection failed
        """
        _conn_status = False
        _conn_retry_count = 0
        _max_retry_count = 3
        while not _conn_status and _conn_retry_count <= _max_retry_count:
            try:
                self.conn = pymysql.connect(host=host, port=port, user=user,
                                            passwd=password, database=database,
                                            charset="utf8mb4", connect_timeout=timeout,
                                            cursorclass=pymysql.cursors.DictCursor,
                                            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS if multi else 0)
                self.cursor = self.conn.cursor()
                _conn_status = True
            except Exception as e:
                _conn_retry_count += 1
                if _conn_retry_count > _max_retry_count:
                    raise e

    def select_one(self, sql, *param):
        """
        select one row
        use parameterd query to prevent SQL injection
        return a dictionary represented one row
        """
        self.cursor.execute(sql, *param)
        return self.cursor.fetchone()

    def select_more(self, sql, *param):
        """
        select multiple rows
        use parameterd query to prevent SQL injection
        return a list of dictionary represented multiple rows
        """
        self.cursor.execute(sql, *param)
        return self.cursor.fetchall()

    def insert(self, sql, *param):
        """
        insert data
        use parameterd query to prevent SQL injection
        return affected number of rows
        """
        self.cursor.execute(sql, *param)
        return self.cursor.lastrowid

    def execute(self, sql, *param):
        """
        write operations
        use parameterd query to prevent SQL injection
        """
        self.cursor.execute(sql, *param)
        return self.cursor.rowcount

    def execute_multi(self, sql, *param):
        """
        execute multiple sql statements, used for db migration
        must init with multi = true
        use parameterd query to prevent SQL injection
        """
        self.cursor.execute(sql, *param)
        rows_affected = list()
        while True:
            rows_affected.append(self.cursor.rowcount)
            if not self.cursor.nextset():
                break
        return rows_affected

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()
