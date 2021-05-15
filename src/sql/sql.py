from settings import (DATABASE_TYPE)
import logging
log = logging.getLogger(__name__)

if DATABASE_TYPE is not None:
    log.info("Using pyodbc")
    try:
        import pyodbc
    except ImportError:
        log.error("pyodbc not loaded")
else:
    log.info("Using sqlite3")
    import sqlite3


class SqlBaseCommands:
    def __init__(self, tables: list):
        self.database = 'data/datatables.db'
        # create a database connection
        conn = self.create_connection(self.database)
        # create tables
        if conn is not None:
            conn.execute("PRAGMA foreign_keys = ON")
            for table in tables:
                conn.execute(table)
        else:
            log.error("Error! cannot create the database connection.")

    @staticmethod
    def create_connection(db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            # If you are testing and debugging, change which lines are commented out. you will have to do this for each sql file
            if DATABASE_TYPE is None:
                conn = sqlite3.connect(db_file)
            else:
                # TODO: Test this and work out how it should be set up. its scuffed rn
                conn = pyodbc.connect(f"DRIVER={os.getenv('SQL_DRIVER', '{SQL Server}')};"
                                      f"SERVER={os.getenv('SQL_SERVER')};"
                                      f"DATABASE={os.getenv('SQL_DATABASE', 'datatables')};"
                                      f"UID={os.getenv('SQL_USERNAME')};"
                                      f"PWD={os.getenv('SQL_PASSWORD')}"
                                      )
            return conn
        except Exception as e:
            log.error(e)

        return conn

    def execute(self, sql: str, parms: tuple = ()) -> list:
        """Executes a single command
        :param sql:
        :param parms:
        :return:
        """
        conn = self.create_connection(self.database)

        if conn is not None:
            try:
                c = conn.cursor()
                c.execute(sql, parms)
                data = c.fetchall()
                conn.commit()
                return data
            except Exception as e:
                log.error(e)

    def execute_many(self, sql: str, parms: list) -> list:
        """Executes a multi line command
        :param sql: the sql command being run
        :param parms: a list of tuples of information
        :return: any output from the sql code
        """
        conn = self.create_connection(self.database)

        if conn is not None:
            try:
                c = conn.cursor()
                c.executemany(sql, parms)
                data = c.fetchall()
                conn.commit()
                return data
            except Exception as e:
                log.error(e)
