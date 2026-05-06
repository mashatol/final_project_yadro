import allure
from google.protobuf.json_format import MessageToDict
import pika
import time
from config import PUSH_CONSOLE_RABBIT
from general.clients.rabbitmq import rabbitmq_connection, create_rabbit_queue
from proto_files import domain_pb2


@allure.step('Deserialize Rabbit message_body')
def deserialize_rabbit_message_body(message_body, event_type):
    event = None
    match event_type:
        case 'push-console_sync.projects.create':
            event = domain_pb2.ProjectCreatedEvent()
        case 'push-console_sync.projects.remove':
            event = domain_pb2.ProjectDeletedEvent()
        case 'push-console_sync.tokens.create':
            event = domain_pb2.ServiceTokenCreatedEvent()
        case 'push-console_sync.tokens.remove':
            event = domain_pb2.ServiceTokenRemovedEvent()
        case 'push-console_sync.signatures.create':
            event = domain_pb2.AndroidSignatureAddedEvent()
        case 'push-console_sync.signatures.remove':
            event = domain_pb2.AndroidSignatureRemovedEvent()
        case 'push-console_sync.apps.create':
            event = domain_pb2.AndroidPackageAddedEvent()
        case 'push-console_sync.apps.remove':
            event = domain_pb2.AndroidPackageRemovedEvent()
        case _:
            return None

    event.ParseFromString(message_body)
    des_message_body = MessageToDict(event)

    return des_message_body

@allure.step("Get sync queue name for projects")
def get_sync_queue_name():
    """Возвращает имя очереди для sync событий"""
    return "test_course.worker-dx-q-events-sync-v1"

