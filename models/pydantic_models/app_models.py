from datetime import datetime
from typing import Optional, List
from pydantic import Field
from models.pydantic_models.common_models import CommonModel, BaseResponseWithDataModel


class AppSignatureModel(CommonModel):
    id: str
    value: str

class AppDataModel(CommonModel):
    id: str
    name: str = Field(min_length = 5, max_length = 50)
    created_at: datetime = Field(description='Дата создания записи в бд')
    package_name: str
    app_signatures: Optional[List[AppSignatureModel]] = Field(default = None)

class GetAppsModel(BaseResponseWithDataModel):
    data: list[AppDataModel]

class GetAppModel(BaseResponseWithDataModel):
    data: AppDataModel