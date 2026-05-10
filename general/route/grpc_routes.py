# general/route/grpc_delete_routes.py

import grpc
from google.protobuf.json_format import ParseDict
from config import GRPC_HOST
from fixtures.ui_fixtures import project_ui
from proto_files import push_console_pb2
from proto_files import push_console_pb2_grpc
from general.requests_wrapper.grpc_request import make_grpc_request


def grpc_delete_app(auth_token, project_id, app_id):
    channel = grpc.insecure_channel(GRPC_HOST)
    stub = push_console_pb2_grpc.DeleteStub(channel)

    metadata = [('authorization', f'Bearer {auth_token}')]

    message = ParseDict(
        {"project_id": project_id,
         "app_id": app_id},
        push_console_pb2.DeleteAppRequest()
    )

    response = make_grpc_request(stub.DeleteApp, message, metadata)

    return response

def grpc_delete_app_signature(auth_token, project_id, app_id, signature_id):
    channel = grpc.insecure_channel(GRPC_HOST)
    stub = push_console_pb2_grpc.DeleteStub(channel)

    metadata = [('authorization', f'Bearer {auth_token}')]

    message = ParseDict(
        {"project_id": project_id,
         "app_id": app_id,
        "signature_id": signature_id},
         push_console_pb2.DeleteSignatureFromAppRequest()
    )

    response = make_grpc_request(stub.DeleteSignatureFromApp, message, metadata)

    return response