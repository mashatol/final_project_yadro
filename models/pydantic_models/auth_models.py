from uuid import UUID

from pydantic import Field

from models.peewee_models.push_console_pw_models import BaseModel
from models.pydantic_models.common_models import BaseResponseWithDataModel, CommonModel
from test_data.enums import UserRole


class RefreshTokenRequestModel(BaseModel):
    refresh_token: str = Field(min_length = 1)

class RefreshTokenDataModel(CommonModel):
    user_id: UUID
    access_token: str
    refresh_token: str
    user_role : UserRole

class RefreshTokenModel(BaseResponseWithDataModel):
    data: RefreshTokenDataModel