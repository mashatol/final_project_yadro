from uuid import UUID
from models.pydantic_models.common_models import BaseResponseWithDataModel, CommonModel
from test_data.enums import UserRole

class RefreshTokensDataModel(CommonModel):
    user_id: UUID
    access_token: str
    refresh_token: str
    user_role : UserRole

class RefreshTokensModel(BaseResponseWithDataModel):
    data: RefreshTokensDataModel