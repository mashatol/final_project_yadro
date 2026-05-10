import allure
from general.route.auth_routes import success_request_change_password, \
    unsuccessful_request_change_password, success_request_logout_user, \
    unsuccessful_request_logout_user, success_request_refresh_tokens, unsuccessful_request_refresh_tokens
from general.checkers.general_checkers import check_rest_response
from models.pydantic_models.common_models import BaseResponseModel
from test_data.enums import ResponseStatus

# pytest_plugins = [
#     'fixtures.auth_fixtures'
# ]

@allure.step('Test success change password')
def test_change_password_success(valid_change_password_body, access_token, user_id, valid_user_data):
    result = success_request_change_password(request_body=valid_change_password_body,
                                             auth_token=access_token,
                                             pydantic_model=BaseResponseModel)

    check_rest_response(
        response = result,
        status = ResponseStatus.OK,
        msg_code = 'push_console_password_changed'
    )

@allure.step('Test unsuccessful change password new password same as old')
def test_change_password_same_as_old(access_token, valid_user_data):
    old_password = valid_user_data['password']
    request_body = {
        "old_password": old_password,
        "new_password": old_password
    }

    result = unsuccessful_request_change_password(
        auth_token=access_token,
        request_body=request_body,
        status_code=409
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_provided_old_password'
    )

@allure.step('Test unsuccessful change password without access_token')
def test_change_password_unauthorized(valid_change_password_body):
    result = unsuccessful_request_change_password(
        auth_token="",
        request_body=valid_change_password_body,
        status_code=401
    )
    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )

@allure.step('Test unsuccessful change password with invalid access_token')
def test_change_password_invalid_token(valid_change_password_body):
    result = unsuccessful_request_change_password(
        auth_token="invalid_token_123",
        request_body=valid_change_password_body,
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )

@allure.step('Test success logout user')
def test_logout_success(access_token, user_id):

    result = success_request_logout_user(
        auth_token=access_token,
        pydantic_model=BaseResponseModel
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_logout_successful'
    )


@allure.step('Test unsuccessful logout user without access_token')
def test_logout_unauthorized():
    result = unsuccessful_request_logout_user(
        auth_token="",
        status_code=401
    )
    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )

@allure.step('Test unsuccessful logout user with invalid access_token')
def test_logout_invalid_token(invalid_access_token):
    result = unsuccessful_request_logout_user(
        auth_token=invalid_access_token,
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )

@allure.step('Test unsuccessful logout user twice - second logout should fail')
def test_logout_twice(access_token):
    result1 = success_request_logout_user(auth_token=access_token)

    check_rest_response(
        response=result1,
        status=ResponseStatus.OK,
        msg_code='push_console_logout_successful'
    )

    result2 = unsuccessful_request_logout_user(
        auth_token=access_token,
        status_code=401
    )

    check_rest_response(
        response=result2,
        status=ResponseStatus.ERROR,
        msg_code='push_console_session_not_found'
    )

@allure.step('Test success refresh_token')
def test_refresh_tokens_success(refresh_token):
    request_body = {"refresh_token": refresh_token}

    result = success_request_refresh_tokens(request_body=request_body)

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_refresh_tokens_successful'
    )

@allure.step('Test unsuccessful refresh invalid refresh_token')
def test_refresh_invalid_refresh_token(invalid_refresh_token):
    request_body = {"refresh_token": invalid_refresh_token}

    result = unsuccessful_request_refresh_tokens(request_body=request_body, status_code = 401)

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )

@allure.step('Test unsuccessful refresh_token with empty request_body')
def test_refresh_token_empty_body():
    request_body = { }

    result = unsuccessful_request_refresh_tokens(request_body=request_body, status_code=401)

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )