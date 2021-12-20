"""
This includes all the functions required for handling all database related functionality
"""
import sqlite3
import logging
import os
from settings import (DATABASE_URI)

conn = sqlite3.connect(DATABASE_URI)
conn.row_factory = sqlite3.Row
c = conn.cursor()

log = logging.getLogger(__name__)

def init_db() -> None:
    """
    Sets up the database with correct tables using information from schema
    """
    for filename in os.listdir("./migrations"):
        if filename.endswith(".sql"):
            with open(f"./migrations/{filename}", "r") as schema_file:
                schema = schema_file.read()
            conn.executescript(schema)
            conn.commit()


# TODO: This can probably be imporved but it works
def select(sql: str, params: tuple = ()) -> list:
    """
    Selects information from a database
    """
    c.execute(sql, params)
    return c.fetchall()


def execute(sql: str, params: tuple) -> None:
    """
    Executes an sql statement and catches integraty errors
    """
    try:
        c.execute(sql, params)
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        log.error("%s", e)