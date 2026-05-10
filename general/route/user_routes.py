import allure
from config import BASE_URL
from general.helpers import add_auth_header_to_default
from general.requests_wrapper.rest_request import make_rest_request
from models.pydantic_models.common_models import BaseResponseModel

GET_USERS_ROUTE = 'push-console/api/v1/users'
APPROVE_USER_ROUTE = 'push-console/api/v1/users/{user_id}/approve'
BLOCK_USER_ROUTE = 'push-console/api/v1/users/{user_id}/block'
PROMOTE_USER_ROUTE = 'push-console/api/v1/users/{user_id}/promote'

@allure.step('Unsuccessful request APPROVE USER')
def unsuccessful_request_approve_user(auth_token, user_id, status_code=403, pydantic_model=BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)

    response = make_rest_request(
        method='POST',
        url=BASE_URL + APPROVE_USER_ROUTE.format(user_id = user_id),
        headers=headers,
        status_code=status_code,
        pydantic_model=pydantic_model
    )
    return response

@allure.step('Unsuccessful request BLOCK USER')
def unsuccessful_request_block_user(auth_token, user_id, status_code=403, pydantic_model=BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)

    response = make_rest_request(method='POST',
                                 url=BASE_URL + BLOCK_USER_ROUTE.format(user_id = user_id),
                                 headers=headers,
                                 status_code=status_code,
                                 pydantic_model=pydantic_model
    )
    return response

@allure.step('Unsuccessful request PROMOTE USER')
def unsuccessful_request_promote_user(auth_token, user_id, status_code=403, pydantic_model=BaseResponseModel):
    headers = add_auth_header_to_default(auth_token)

    response = make_rest_request(method='POST',
                                 url=BASE_URL + PROMOTE_USER_ROUTE.format(user_id = user_id),
                                 headers=headers,
                                 status_code=status_code,
                                 pydantic_model=pydantic_model
    )
    return response