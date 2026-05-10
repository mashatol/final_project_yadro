from models.pydantic_models.common_models import CommonModel, BaseResponseWithDataModel, MetaModel

class GetProjectsModel(BaseResponseWithDataModel):
    _meta: MetaModel

class CreateProjectDataModel(CommonModel):
    project_id: str

class CreateProjectModel(BaseResponseWithDataModel):
    data: CreateProjectDataModel

