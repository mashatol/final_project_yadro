import os
import json

def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as f:
        return json.load(f)

config = load_config('config_file_local.json')
EMAIL = os.getenv('EMAIL', config['EMAIL'])
PASSWORD = os.getenv('PASSWORD', config['PASSWORD'])
BASE_URL = config['BASE_URL']
GRPC_HOST = config['GRPC_HOST']

PUSH_CONSOLE_POSTGRES_DB = {
    'host': config['PUSH_CONSOLE_POSTGRES_HOST'],
    'port': config['PUSH_CONSOLE_POSTGRES_PORT'],
    'database': config['PUSH_CONSOLE_POSTGRES_DATABASE'],
    'user': config['PUSH_CONSOLE_POSTGRES_USER'],
    'password': config['PUSH_CONSOLE_POSTGRES_PASSWORD']
}

PUSH_CONSOLE_CLICKHOUSE_DB = {
    'host': config['PUSH_CONSOLE_CLICKHOUSE_HOST'],
    'port': config['PUSH_CONSOLE_CLICKHOUSE_PORT'],
    'user': config['PUSH_CONSOLE_CLICKHOUSE_USER'],
    'password': config['PUSH_CONSOLE_CLICKHOUSE_PASSWORD']
}

PUSH_CONSOLE_REDIS_DB = {
    'host': config['PUSH_CONSOLE_REDIS_HOST'],
    'port': config['PUSH_CONSOLE_REDIS_PORT'],
    'password': config['PUSH_CONSOLE_REDIS_PASSWORD']
}

PUSH_CONSOLE_RABBIT = {
    'host': config['PUSH_CONSOLE_RABBIT_HOST'],
    'port': config['PUSH_CONSOLE_RABBIT_PORT'],
    'virtual_host': config['PUSH_CONSOLE_RABBIT_VHOST'],
    'username': config['PUSH_CONSOLE_RABBIT_USER'],
    'password': config['PUSH_CONSOLE_RABBIT_PASSWORD']
}
