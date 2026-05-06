from contextlib import contextmanager

import pika
import pytest
from pika.exceptions import AMQPError

from config import PUSH_CONSOLE_RABBIT


@contextmanager
def rabbitmq_connection(message_broker):
    conn = None
    channel = None
    try:
        creds = pika.PlainCredentials(username=message_broker['username'], password=message_broker['password'])
        params = pika.ConnectionParameters(host=message_broker['host'], port=message_broker['port'],
                                           virtual_host=message_broker['virtual_host'], credentials=creds)
        conn = pika.BlockingConnection(parameters=params)
        channel = conn.channel()
        yield channel
    except AMQPError as err:
        pytest.fail(f"RabbitMQ connection: {message_broker} failed. Reason: {err}")
    finally:
        channel.close()
        conn.close()


def create_rabbit_queue(exchange, routing_key, message_broker=PUSH_CONSOLE_RABBIT):
    with rabbitmq_connection(message_broker=message_broker) as channel:
        def_queue = channel.queue_declare('', auto_delete=True, durable=True,
                                          arguments={"x-queue-type": "classic", "x-expires": 60000})
        queue_name = def_queue.method.queue
        channel.queue_bind(queue=queue_name, exchange=exchange, routing_key=routing_key)

        return queue_name
