
import grpc
import pytest
from google.protobuf.json_format import MessageToDict

def make_grpc_request(stub_method, request_message, metadata=None, expected_status_code=200):
    try:
        response = stub_method(request_message, metadata=metadata)
        return MessageToDict(response, preserving_proto_field_name=True)

    except grpc.RpcError as error:
        if error.code().value[0] != expected_status_code:
            pytest.fail(f"Expected status {expected_status_code}, got {error.code().value[0]}")
        return {'error': {'code': error.code().value[0], 'message': error.details()}}

