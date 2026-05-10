import allure
from config import BASE_URL, EMAIL, PASSWORD
from general.helpers import add_auth_header_to_default
from general.requests_wrapper.rest_request import make_rest_request
from models.pydantic_models.common_models import BaseResponseModel

LOGIN_USER_ROUTE = 'push-console/api/v1/auth/login'
CHANGE_PASSWORD_ROUTE = 'push-console/api/v1/auth/password/change'
AUTH_LOGOUT_ROUTE = 'push-console/api/v1/auth/logout'
AUTH_PASSWORD_RESET_ROUTE = 'push-console/api/v1/auth/password/reset'
REFRESH_TOKENS_ROUTE = 'push-console/api/v1/auth/refresh'

@allure.step('Successful request POST LOGIN')
def success_request_login_user():
    request_body = {
        "email": EMAIL,
        "password": PASSWORD
    }
    response = make_rest_request(url =BASE_URL + LOGIN_USER_ROUTE, json = request_body)
    return response

@allure.step('Successful request POST LOGOUT')
def success_request_logout_user(auth_token, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(url=BASE_URL + AUTH_LOGOUT_ROUTE,
                                 headers=headers,
                                 pydantic_model=pydantic_model)

    return response

@allure.step('Unsuccessful request POST LOGOUT')
def unsuccessful_request_logout_user(auth_token, status_code = None, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)
    response = make_rest_request(url=BASE_URL + AUTH_LOGOUT_ROUTE,
                                 headers=headers,
                                 status_code=status_code,
                                 pydantic_model=pydantic_model)

    return response

@allure.step("Successful request POST CHANGE PASSWORD")
def success_request_change_password(request_body, auth_token, pydantic_model=BaseResponseModel):
    headers = add_auth_header_to_default(auth_token=auth_token)
    response = make_rest_request(url=BASE_URL+ CHANGE_PASSWORD_ROUTE,
                                 json = request_body,
                                 headers = headers,
                                 pydantic_model=pydantic_model)
    return response


@allure.step("Unsuccessful request POST CHANGE PASSWORD")
def unsuccessful_request_change_password(auth_token, request_body=None, status_code=None, pydantic_model = BaseResponseModel):
    headers = add_auth_header_to_default(auth_token=auth_token)
    response = make_rest_request(url=BASE_URL+ CHANGE_PASSWORD_ROUTE,
                                 json = request_body, headers = headers,
                                 status_code=status_code,
                                 pydantic_model=pydantic_model)
    return response

