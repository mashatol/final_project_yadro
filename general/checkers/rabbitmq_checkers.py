import allure
import pytest

from config import PUSH_CONSOLE_RABBIT
from general.clients.rabbitmq import rabbitmq_connection
from general.helpers.rabbitmq_helpers import deserialize_rabbit_message_body


@allure.step('Check rabbit event')
def check_rabbit_event(queue_name, expected_event_type, message_broker=PUSH_CONSOLE_RABBIT):
    result = None
    with rabbitmq_connection(message_broker=message_broker) as channel:
        for _ in range(500):
            method_frame, properties, message_body = channel.basic_get(queue=queue_name, auto_ack=False)
            if method_frame is None:
                continue
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            if properties.type == expected_event_type:
                result = deserialize_rabbit_message_body(message_body=message_body, event_type=expected_event_type)
                print(result)  # need to check
                break
        channel.queue_delete(queue=queue_name)

        if result is None:
            pytest.fail(f"Not found event_type = {expected_event_type} in RabbitMQ: {message_broker}")