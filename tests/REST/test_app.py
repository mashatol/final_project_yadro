import pytest

from fixtures.app_fixtures import app_setup
from fixtures.auth_fixtures import access_token
from general.checkers.general_checkers import general_checker, check_rest_response
from general.helpers import add_auth_header_to_default
from general.route.app_routes import success_request_create_app, unsuccessful_request_create_app, \
    success_request_get_apps, unsuccessful_request_get_apps, success_request_get_app, unsuccessful_request_get_app, \
    success_request_update_app, unsuccessful_request_update_app, success_request_delete_app, \
    unsuccessful_request_delete_app
from general.utils import rand_app_name, rand_package_name, rand_app_signature
from models.pydantic_models.app_models import GetAppsModel
from test_data.enums import ResponseStatus

pytest_plugins = [
    'fixtures.auth_fixtures',
    'fixtures.project_fixtures',
    'fixtures.app_fixtures'
]


def test_create_app_success(create_app):
    auth_data, project_data, response, app_data = create_app

    check_rest_response(
        response=response,
        status=ResponseStatus.OK,
        msg_code='push_console_app_successful_created'
    )

def test_create_app_missing_fields(app_setup, missing_fields):
    result = unsuccessful_request_create_app(
        auth_token=app_setup['token'],
        project_id=app_setup['project_id'],
        request_body=missing_fields,
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='go_validation'
    )


def test_create_app_invalid_name(app_setup, invalid_app_name_body):
    result = unsuccessful_request_create_app(
        auth_token=app_setup['token'],
        project_id=app_setup['project_id'],
        request_body=invalid_app_name_body,
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='go_validation'
    )

@pytest.mark.skip('Backend return 500 instead of 422')
def test_create_app_invalid_signature(app_setup, invalid_app_signature_body):
    result = unsuccessful_request_create_app(
        auth_token=app_setup['token'],
        project_id=app_setup['project_id'],
        request_body=invalid_app_signature_body,
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='go_validation'
    )


def test_get_apps_success(create_app):
    auth_data, project_data, create_response, app_data = create_app
    project_id = project_data['project_id']

    result = success_request_get_apps(
        auth_token=auth_data['access_token'],
        project_id=project_id,
        pydantic_model=GetAppsModel
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_apps_successful_getting'
    )


def test_get_apps_invalid_project_id(create_authorized_user, invalid_project_id):
    _, auth_data = create_authorized_user

    result = unsuccessful_request_get_apps(
        auth_token=auth_data['access_token'],
        project_id=invalid_project_id,
        status_code=404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_project_not_found'
    )


def test_get_apps_unauthorized(create_project_with_deletion):
    _, project_data = create_project_with_deletion
    project_id = project_data['project_id']

    result = unsuccessful_request_get_apps(
        auth_token="",
        project_id=project_id,
        status_code = 401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )


def test_get_app_success(create_app):
    auth_data, project_data, create_response, app_data = create_app
    project_id = project_data['project_id']
    app_id = app_data['app_id']

    result = success_request_get_app(
        auth_token=auth_data['access_token'],
        project_id=project_id,
        app_id=app_id
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_app_successful_getting'
    )

@pytest.mark.skip("Return 500 instead of 404")
def test_get_app_not_found(create_app, not_found_app_id):
    auth_data, project_data, _, _ = create_app
    project_id = project_data['project_id']

    result = unsuccessful_request_get_app(
        auth_token=auth_data['access_token'],
        project_id=project_id,
        app_id=not_found_app_id,
        status_code = 404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_app_not_found'
    )

def test_get_app_unauthorized(create_app):
    _, project_data, _, app_data = create_app
    project_id = project_data['project_id']
    app_id = app_data['app_id']

    result = unsuccessful_request_get_app(
        auth_token="",
        project_id=project_id,
        app_id=app_id,
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )


def test_update_app_success(app_setup, valid_update_body):

    result = success_request_update_app(
        auth_token=app_setup['token'],
        project_id=app_setup['project_id'],
        app_id=app_setup['app_id'],
        request_body=valid_update_body
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_app_success_update'
    )


def test_update_app_same_name(app_setup):
    request_body = {"name": app_setup['app_name']}

    result = success_request_update_app(
        auth_token=app_setup['token'],
        project_id=app_setup['project_id'],
        app_id=app_setup['app_id'],
        request_body=request_body
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_app_success_update'
    )


def test_update_app_invalid_name(app_setup, invalid_update_body):

    result = unsuccessful_request_update_app(
        auth_token=app_setup['token'],
        project_id=app_setup['project_id'],
        app_id=app_setup['app_id'],
        request_body=invalid_update_body,
        status_code=422
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='go_validation'
    )

@pytest.mark.skip('Return 500 instead of 404')
def test_update_app_not_found(create_project_with_deletion, valid_update_body, not_found_app_id):
    auth_data, project_data = create_project_with_deletion

    result = unsuccessful_request_update_app(
        auth_token=auth_data['access_token'],
        project_id=project_data['project_id'],
        app_id=not_found_app_id,
        request_body=valid_update_body,
        status_code=404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_app_not_found'
    )


def test_update_app_invalid_project_id(create_app, valid_update_body, invalid_project_id):
    auth_data, _, _, app_data = create_app

    result = unsuccessful_request_update_app(
        auth_token=auth_data['access_token'],
        project_id=invalid_project_id,
        app_id=app_data['app_id'],
        request_body=valid_update_body,
        status_code=404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_project_not_found'
    )


def test_update_app_unauthorized(app_setup, valid_update_body):
    result = unsuccessful_request_update_app(
        auth_token="",
        project_id=app_setup['project_id'],
        app_id=app_setup['app_id'],
        request_body=valid_update_body,
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )


def test_update_app_invalid_token(app_setup, valid_update_body, invalid_token):
    result =unsuccessful_request_update_app(
        auth_token=invalid_token,
        project_id=app_setup['project_id'],
        app_id=app_setup['app_id'],
        request_body=valid_update_body,
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )

def test_update_app_empty_body(app_setup):
    result = unsuccessful_request_update_app(
        auth_token=app_setup['token'],
        project_id=app_setup['project_id'],
        app_id=app_setup['app_id'],
        request_body={},
        status_code=422
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='go_validation'
    )


def test_delete_app_success(app_setup_delete):
    result = success_request_delete_app(
        auth_token=app_setup_delete['token'],
        project_id=app_setup_delete['project_id'],
        app_id=app_setup_delete['app_id']
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_app_successful_deleted'
    )


@pytest.mark.skip('Return 500 instead of 404')
def test_delete_app_not_found(app_setup_delete, not_found_app_id):
    result = unsuccessful_request_delete_app(
        auth_token=app_setup_delete['token'],
        project_id=app_setup_delete['project_id'],
        app_id=not_found_app_id,
        status_code=404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_app_not_found'
    )


def test_delete_app_invalid_project_id(create_app_without_deletion, invalid_project_id):
    auth_data, _, _, app_data = create_app_without_deletion

    result = unsuccessful_request_delete_app(
        auth_token=auth_data['access_token'],
        project_id= invalid_project_id,
        app_id=app_data['app_id'],
        status_code=404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_project_not_found'
    )

def test_delete_app_unauthorized(app_setup_delete):
    result = unsuccessful_request_delete_app(
        auth_token="",
        project_id=app_setup_delete['project_id'],
        app_id=app_setup_delete['app_id'],
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )


def test_delete_app_invalid_token(app_setup_delete):
    result = unsuccessful_request_delete_app(
        auth_token="invalid_token_123",
        project_id=app_setup_delete['project_id'],
        app_id=app_setup_delete['app_id'],
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )


def test_delete_app_twice(app_setup_delete):
    result1 = success_request_delete_app(
        auth_token=app_setup_delete['token'],
        project_id=app_setup_delete['project_id'],
        app_id=app_setup_delete['app_id']
    )

    check_rest_response(response=result1,
                        status=ResponseStatus.OK,
                        msg_code='push_console_app_successful_deleted'
                        )

    result2 = unsuccessful_request_delete_app(
        auth_token=app_setup_delete['token'],
        project_id=app_setup_delete['project_id'],
        app_id=app_setup_delete['app_id'],
        status_code=404
    )

    check_rest_response(response=result2,
                        status=ResponseStatus.ERROR,
                        msg_code='push_console_app_not_found'
    )



