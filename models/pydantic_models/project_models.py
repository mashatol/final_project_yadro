from datetime import datetime

from pydantic import Field, ConfigDict, BaseModel

from models.pydantic_models.common_models import CommonModel, BaseResponseWithDataModel, MetaModel


class GetProjectsDataModel(CommonModel):
    project_id: str
    name: str = Field(min_length=5, max_length=50)

class GetProjectsModel(BaseResponseWithDataModel):
    _meta: MetaModel


class CreateProjectDataModel(CommonModel):
    project_id: str

class CreateProjectModel(BaseResponseWithDataModel):
    data: CreateProjectDataModel


class AppModel(CommonModel):
    id: str
    name: str = Field(min_length=5, max_length=50)
    created_at: datetime = Field(description='Дата создания записи в бд')
    package_name: str

class GetProjectByIdDataModel(CommonModel):
    project_id: str
    name: str = Field(min_length=5, max_length=50)
    service_tokens: list[str]
    apps: list[AppModel]

class GetProjectByIdModel(BaseResponseWithDataModel):
    data: GetProjectByIdDataModel

