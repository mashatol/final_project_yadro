import allure

from config import BASE_URL
from general.requests_wrapper import make_rest_request
from general.helpers import add_auth_header_to_default
from models.pydantic_models.app_models import GetAppsModel, GetAppModel
from models.pydantic_models.common_models import BaseResponseModel

GET_APPS_ROUTE = 'push-console/api/v1/projects/{id}/apps'
CREATE_APP_ROUTE = 'push-console/api/v1/projects/{id}/apps'
GET_APP_ROUTE = 'push-console/api/v1/projects/{project_id}/apps/{app_id}'
DELETE_APP_ROUTE = 'push-console/api/v1/projects/{project_id}/apps/{app_id}'
UPDATE_APP_ROUTE = 'push-console/api/v1/projects/{project_id}/apps/{app_id}'

@allure.step('Successful request for GET APPS')
def success_request_get_apps(auth_token, project_id, pydantic_model= GetAppsModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method='GET',
                                 url =BASE_URL + GET_APPS_ROUTE.format(id=project_id),
                                 headers= headers,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Unsuccessful request for GET APPS')
def unsuccessful_request_get_apps(auth_token, project_id, status_code = None, pydantic_model= BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method='GET',
                                 url =BASE_URL + GET_APPS_ROUTE.format(id=project_id),
                                 headers= headers,
                                 status_code= status_code,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Unsuccessful request for CREATE APP')
def unsuccessful_request_create_app(auth_token, request_body, project_id, pydantic_model = BaseResponseModel ):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(url=BASE_URL + CREATE_APP_ROUTE.format(id=project_id),
                                 headers = headers,
                                 json = request_body,
                                 status_code = 422,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Successful request for CREATE APP')
def success_request_create_app(auth_token, request_body, project_id, pydantic_model = BaseResponseModel ):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(url=BASE_URL + CREATE_APP_ROUTE.format(id=project_id),
                                 headers = headers,
                                 json = request_body,
                                 status_code = 201,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Successful request for GET APP')
def success_request_get_app(auth_token, project_id, app_id, pydantic_model = GetAppModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method = 'GET',
                                 url =BASE_URL + GET_APP_ROUTE.format(project_id = project_id, app_id =app_id),
                                 headers=headers,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Unsuccessful request for GET APP')
def unsuccessful_request_get_app(auth_token, project_id, app_id, status_code = None, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method = 'GET',
                                 url =BASE_URL + GET_APP_ROUTE.format(project_id = project_id, app_id =app_id),
                                 headers=headers,
                                 status_code=status_code,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Successful request for UPDATE APP')
def success_request_update_app(auth_token, project_id, app_id, request_body, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method = 'PUT',
                                 url =BASE_URL + UPDATE_APP_ROUTE.format(project_id = project_id, app_id =app_id),
                                 headers=headers,
                                 json = request_body,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Unsuccessful request for UPDATE APP')
def unsuccessful_request_update_app(auth_token, project_id, app_id, request_body, status_code = None, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method = 'PUT',
                                 url =BASE_URL + UPDATE_APP_ROUTE.format(project_id = project_id, app_id =app_id),
                                 headers=headers,
                                 json = request_body,
                                 status_code = status_code,
                                 pydantic_model=pydantic_model)
    return response

@allure.step('Successful request for DELETE APP')
def success_request_delete_app(auth_token, project_id, app_id, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method = 'DELETE',
                                 url =BASE_URL + DELETE_APP_ROUTE.format(project_id = project_id, app_id =app_id),
                                 headers=headers,
                                 pydantic_model=pydantic_model)
    return response


@allure.step('Unsuccessful request for DELETE APP')
def unsuccessful_request_delete_app(auth_token, project_id, app_id, status_code = None, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(method = 'DELETE',
                                 url =BASE_URL + DELETE_APP_ROUTE.format(project_id = project_id, app_id =app_id),
                                 status_code=status_code,
                                 headers=headers,
                                 pydantic_model=pydantic_model)
    return response

