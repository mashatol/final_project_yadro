from contextlib import contextmanager
import psycopg2
import pytest
from config import PUSH_CONSOLE_POSTGRES_DB
@contextmanager
def postgres_db_connection(database):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**database)
        cursor = conn.cursor()
        yield conn, cursor
    except psycopg2.OperationalError as err:
        pytest.fail(reason=f"Postgres database: {database}. Unexpected error: {err}")
    finally:
        cursor.close()
        conn.close()
def execute_postgres_non_select(query, params=None, database=PUSH_CONSOLE_POSTGRES_DB):
    with postgres_db_connection(database=database) as (conn, cursor):
        cursor.execute(query, params)
        conn.commit()
def execute_postgres_select_all(query, params=None, database=PUSH_CONSOLE_POSTGRES_DB):
    with postgres_db_connection(database=database) as (conn, cursor):
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [col[0] for col in (cursor.description or [])]
        return [dict(zip(columns, row)) for row in rows]
