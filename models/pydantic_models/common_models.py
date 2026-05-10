from typing import Optional, Any, TypeVar
from pydantic import BaseModel, ConfigDict
from test_data.enums import ResponseStatus


class CommonModel(BaseModel):
    """Model for config."""

    model_config = ConfigDict(extra='forbid')


class BaseResponseModel(CommonModel):
    """Model for base REST responses with fields 'status', 'msg_code' and optional 'data' ."""
    status: ResponseStatus
    msg_code: str
    data: Optional[Any] = None

class BaseResponseWithDataModel(BaseResponseModel):
    """Model for REST responses with field 'data'."""
    data: None


class MetaModel(BaseModel):
    current_page: int
    page_count: int
    per_page: int
    total_count: int
