from general.helpers.postgres_db_helpers import get_user_by_id_from_pg
from general.route.auth_routes import success_request_change_password, \
    unsuccessful_request_change_password, success_request_logout_user, \
    unsuccessful_request_logout_user
from general.checkers.general_checkers import check_rest_response
from models.pydantic_models.common_models import BaseResponseModel
from test_data.enums import ResponseStatus

pytest_plugins = [
    'fixtures.auth_fixtures'
]


def test_change_password_success(valid_change_password_body, access_token, user_id, valid_user_data):
    db_user_before = get_user_by_id_from_pg(user_id=user_id)

    result = success_request_change_password(request_body=valid_change_password_body,
                                             auth_token=access_token,
                                             pydantic_model=BaseResponseModel)

    check_rest_response(
        response = result,
        status = ResponseStatus.OK,
        msg_code = 'push_console_password_changed'
    )
    db_user_after = get_user_by_id_from_pg(user_id=user_id)

    print(f"PostreSQL user BEFORE: {db_user_before}")
    print(f"PostreSQL user AFTER: {db_user_after}")

def test_change_password_missing_field(change_password_no_old_or_new_password, access_token):

    result = unsuccessful_request_change_password(request_body=change_password_no_old_or_new_password,
                                                  auth_token=access_token,
                                                  status_code=422,
                                                  pydantic_model=BaseResponseModel)
    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='go_validation'
    )


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



def test_logout_without_token():
    result = unsuccessful_request_logout_user(
        auth_token="",
        status_code=401
    )
    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )

def test_logout_invalid_token_formats(invalid_token):
    result = unsuccessful_request_logout_user(
        auth_token=invalid_token,
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )


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