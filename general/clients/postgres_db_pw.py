from contextlib import contextmanager

import peewee
import pytest

from config import PUSH_CONSOLE_POSTGRES_DB


@contextmanager
def postgres_db_pw_connection(database):
    db = None
    try:
        db = peewee.PostgresqlDatabase(**database)
        db.connect()
        yield db
    except peewee.PeeweeException as err:
        pytest.fail(f'Postgres Peewee error: {err}')
    finally:
        db.close()


def push_console_db_connection(database=PUSH_CONSOLE_POSTGRES_DB):
    with postgres_db_pw_connection(database=database) as db:
        return db
