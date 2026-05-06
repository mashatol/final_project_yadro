from contextlib import contextmanager

import pytest
import redis

from config import PUSH_CONSOLE_REDIS_DB


@contextmanager
def redis_db_connection(database):
    conn = None
    try:
        conn = redis.Redis(**database, decode_responses=True)
        yield conn
    except redis.exceptions.ConnectionError as err:
        pytest.fail(reason=f"Redis database: {database}. Unexpected error: {err}")
    finally:
        conn.close()


def get_redis_data(key, database=PUSH_CONSOLE_REDIS_DB):
    with redis_db_connection(database=database) as conn:
        value = conn.get(key)
        return value