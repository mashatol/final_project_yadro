from random import choice

from config import BASE_URL
from general.requests_wrapper.rest_request import make_rest_request
import allure
from general.helpers import add_auth_header_to_default
from models.pydantic_models.common_models import BaseResponseModel
from models.pydantic_models.project_models import CreateProjectModel, GetProjectsModel

CREATE_GET_PROJECT_ROUTE= 'push-console/api/v1/projects'
ADD_SERVICE_TOKEN_ROUTE= 'push-console/api/v1/projects/{id}/service-tokens'
PROJECTS_ID_ROUTE = 'push-console/api/v1/projects/{id}'
DELETE_TOKEN_ROUTE = 'push-console/api/v1/projects/{id}/service-tokens/{value}'

@allure.step('Successful request for GET PROJECTS')
def success_request_get_projects(auth_token, pydantic_model= GetProjectsModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method='GET',
                                 url =BASE_URL + CREATE_GET_PROJECT_ROUTE,
                                 headers= headers,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Successful request for CREATE PROJECT')
def success_request_create_project(request_body,auth_token, pydantic_model = CreateProjectModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(url =BASE_URL + CREATE_GET_PROJECT_ROUTE,
                                 json= request_body,
                                 headers= headers,
                                 status_code=201,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Successful request for DELETE PROJECT')
def success_request_delete_project(auth_token, project_id, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method='DELETE',
                                 url=BASE_URL + PROJECTS_ID_ROUTE.format(id=project_id),
                                 headers=headers,
                                 status_code=200,
                                 pydantic_model=pydantic_model)

    return response

@allure.step('Unsuccessful request for DELETE PROJECT')
def unsuccessful_request_delete_project(auth_token, project_id, status_code = None, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method='DELETE',
                                 url=BASE_URL + PROJECTS_ID_ROUTE.format(id=project_id),
                                 headers=headers,
                                 status_code= status_code,
                                 pydantic_model=pydantic_model)

    return response

@allure.step('Successful request for UPDATE PROJECTS/{project_id}')
def success_request_update_project(auth_token, project_id, request_body, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method = 'PUT',
                                 url = BASE_URL + PROJECTS_ID_ROUTE.format(id = project_id),
                                 json = request_body,
                                 headers = headers,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Unsuccessful request for UPDATE PROJECTS/{project_id}')
def unsuccessful_request_update_project(auth_token, project_id, request_body, pydantic_model = BaseResponseModel, status_code = None):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method = 'PUT',
                                 url = BASE_URL + PROJECTS_ID_ROUTE.format(id = project_id),
                                 json = request_body,
                                 headers = headers,
                                 status_code=status_code,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Successful request for ADD SERVICE TOKEN')
def success_request_add_token(auth_token, project_id, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(url =BASE_URL + ADD_SERVICE_TOKEN_ROUTE.format(id=project_id),
                                 headers=headers,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Unsuccessful request for ADD SERVICE TOKEN')
def unsuccessful_request_add_token(auth_token, project_id, status_code = None, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(url =BASE_URL + ADD_SERVICE_TOKEN_ROUTE.format(id=project_id),
                                 headers=headers,
                                 status_code=status_code,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Successful request for DELETE SERVICE TOKEN')
def success_request_delete_token(auth_token, project_id, token_value, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method= 'DELETE',
                                 url =BASE_URL + DELETE_TOKEN_ROUTE.format(id=project_id, value = token_value),
                                 headers=headers,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Unsuccessful request for DELETE SERVICE TOKEN')
def unsuccessful_request_delete_token(auth_token, project_id, token_value, status_code = None, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method= 'DELETE',
                                 url =BASE_URL + DELETE_TOKEN_ROUTE.format(id=project_id, value = token_value),
                                 headers=headers,
                                 status_code=status_code,
                                 pydantic_model=pydantic_model)
    return response