from enum import StrEnum


class ResponseStatus(StrEnum):
    OK = 'OK'
    ERROR = 'ERROR'


class UserRole(StrEnum):
    USER = 'USER'
    BLOCKED = 'BLOCKED'
    SUPER_ADMIN = 'SUPER_ADMIN'


class UserQueryParam(StrEnum):
    ROLE = 'role'
