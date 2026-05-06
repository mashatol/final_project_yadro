from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectCreatedEvent(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ProjectDeletedEvent(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AndroidPackageAddedEvent(_message.Message):
    __slots__ = ("id", "package_name", "project_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    package_name: str
    project_id: str
    def __init__(self, id: _Optional[str] = ..., package_name: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class AndroidPackageRemovedEvent(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AndroidSignatureAddedEvent(_message.Message):
    __slots__ = ("id", "android_package_id", "value")
    ID_FIELD_NUMBER: _ClassVar[int]
    ANDROID_PACKAGE_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    id: str
    android_package_id: str
    value: str
    def __init__(self, id: _Optional[str] = ..., android_package_id: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class AndroidSignatureRemovedEvent(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ServiceTokenCreatedEvent(_message.Message):
    __slots__ = ("value", "project_id")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    value: str
    project_id: str
    def __init__(self, value: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class ServiceTokenRemovedEvent(_message.Message):
    __slots__ = ("value", "project_id")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    value: str
    project_id: str
    def __init__(self, value: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...
