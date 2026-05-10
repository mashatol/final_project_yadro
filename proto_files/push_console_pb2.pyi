from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CODE_UNSPECIFIED: _ClassVar[ErrorCode]
    BAD_REQUEST: _ClassVar[ErrorCode]
    BAD_TOKEN: _ClassVar[ErrorCode]
    NOT_FOUND: _ClassVar[ErrorCode]
    ACCESS_DENIED: _ClassVar[ErrorCode]
    CONFLICT: _ClassVar[ErrorCode]
    INTERNAL_ERROR: _ClassVar[ErrorCode]
ERROR_CODE_UNSPECIFIED: ErrorCode
BAD_REQUEST: ErrorCode
BAD_TOKEN: ErrorCode
NOT_FOUND: ErrorCode
ACCESS_DENIED: ErrorCode
CONFLICT: ErrorCode
INTERNAL_ERROR: ErrorCode

class DeleteAppRequest(_message.Message):
    __slots__ = ("project_id", "app_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    app_id: str
    def __init__(self, project_id: _Optional[str] = ..., app_id: _Optional[str] = ...) -> None: ...

class DeleteSignatureFromAppRequest(_message.Message):
    __slots__ = ("project_id", "app_id", "signature_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    app_id: str
    signature_id: str
    def __init__(self, project_id: _Optional[str] = ..., app_id: _Optional[str] = ..., signature_id: _Optional[str] = ...) -> None: ...

class DeleteReply(_message.Message):
    __slots__ = ("error", "success")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: DeleteError
    success: DeleteSuccess
    def __init__(self, error: _Optional[_Union[DeleteError, _Mapping]] = ..., success: _Optional[_Union[DeleteSuccess, _Mapping]] = ...) -> None: ...

class DeleteError(_message.Message):
    __slots__ = ("code", "error_message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    error_message: str
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class DeleteSuccess(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
