from config import BASE_URL
from general.checkers.general_checkers import general_checker, check_rest_response
from general.helpers import add_auth_header_to_default
from general.helpers.postgres_db_helpers import get_project_by_id_from_pg
from general.requests_wrapper import make_rest_request
from general.route.project_routes import success_request_update_project, \
    unsuccessful_request_update_project, \
    success_request_delete_project, unsuccessful_request_delete_project, PROJECTS_ID_ROUTE, success_request_add_token, \
    unsuccessful_request_add_token
from general.utils import rand_project_name
from test_data.enums import ResponseStatus
import pytest

pytest_plugins = [
    'fixtures.auth_fixtures',
    'fixtures.project_fixtures'
]

def test_delete_project_success(create_project):
    auth_data, project = create_project
    project_id = project['data']['project_id']

    result = success_request_delete_project(auth_token=auth_data['access_token'],
                                            project_id=project_id)
    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_project_successful_deleted'
    )

def test_delete_project_invalid_id(create_project, invalid_project_id):
    auth_data, project = create_project
    project_id = invalid_project_id

    db_projects_before = get_project_by_id_from_pg(auth_data['user_id'])
    count_before = len(db_projects_before)
    result = unsuccessful_request_delete_project(auth_token=auth_data['access_token'],
                                                 status_code = 404,
                                                project_id=project_id)
    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_project_not_found'
    )
    db_projects_after = get_project_by_id_from_pg(auth_data['user_id'])
    general_checker(actual=len(db_projects_after), expected=count_before)

def test_delete_project_unauthorized(create_project):
    auth_data, project = create_project
    project_id = project['data']['project_id']

    result = unsuccessful_request_delete_project(
        auth_token="",
        project_id=project_id,
        status_code = 401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )

def test_delete_project_invalid_token(create_project, invalid_token):
    auth_data, project = create_project
    project_id = project['data']['project_id']

    result = unsuccessful_request_delete_project(
        auth_token=invalid_token,
        project_id=project_id,
        status_code = 401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )


def test_delete_already_deleted_project(create_project):
    auth_data, project = create_project
    project_id = project['data']['project_id']

    success_request_delete_project(
        auth_token=auth_data['access_token'],
        project_id=project_id
    )

    result = unsuccessful_request_delete_project(
        auth_token=auth_data['access_token'],
        project_id=project_id,
        status_code = 404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_project_not_found'
    )

def test_update_project_success(update_project_data):
    new_name = rand_project_name()

    db_project_before = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_before['name'], expected=update_project_data['old_name'])

    result = success_request_update_project(auth_token = update_project_data['auth_token'],
                                            request_body = {"name": new_name},
                                            project_id = update_project_data['project_id'])
    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_project_successful_updated'
    )

    db_project_after = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_after['name'], expected=new_name)

def test_update_project_invalid_name(update_project_data, invalid_project_name):

    db_project_before = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_before['name'], expected= update_project_data['old_name'])

    result = unsuccessful_request_update_project(auth_token = update_project_data['auth_token'],
                                            request_body = {"name": invalid_project_name},
                                            project_id = update_project_data['project_id'],
                                                 status_code=422)
    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='go_validation'
    )
    db_project_after = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_after['name'], expected=update_project_data['old_name'])


def test_update_project_unauthorized(update_project_data):
    result = unsuccessful_request_update_project(
        auth_token="",
        request_body={"name": rand_project_name()},
        project_id=update_project_data['project_id'],
        status_code=401
    )

    check_rest_response(response=result,
                        status=ResponseStatus.ERROR,
                        msg_code='general_unauthorized')


def test_update_project_invalid_token(update_project_data, invalid_token):
    result = unsuccessful_request_update_project(
        auth_token=invalid_token,
        request_body={"name": rand_project_name()},
        project_id=update_project_data['project_id'],
        status_code=401
    )

    check_rest_response(response=result,
                        status=ResponseStatus.ERROR,
                        msg_code='general_bad_token')


def test_update_project_invalid_id_format(create_authorized_user, invalid_project_id):
    _, auth_data = create_authorized_user

    result = unsuccessful_request_update_project(
        auth_token=auth_data['access_token'],
        request_body={"name": rand_project_name()},
        project_id=invalid_project_id,
        status_code=404
    )

    check_rest_response(response=result,
                        status=ResponseStatus.ERROR,
                        msg_code='push_console_project_not_found')

def test_update_project_empty_name(update_project_data, no_project_name):
    db_before = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_before['name'], expected=update_project_data['old_name'])

    result = unsuccessful_request_update_project(
        auth_token=update_project_data['auth_token'],
        request_body=no_project_name,
        project_id=update_project_data['project_id'],
        status_code=422
    )

    check_rest_response(response=result,
                        status=ResponseStatus.ERROR,
                        msg_code='go_validation')


@pytest.mark.skip("Return 500 instead of 422")
def test_update_invalid_project_name(update_project_data, invalid_project_name):
    db_before = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_before['name'], expected=update_project_data['old_name'])

    result = unsuccessful_request_update_project(
        auth_token=update_project_data['auth_token'],
        request_body=invalid_project_name,
        project_id=update_project_data['project_id'],
        status_code=422
    )

    check_rest_response(response=result,
                        status=ResponseStatus.ERROR,
                        msg_code='go_validation')

def test_add_service_token_success(create_project_with_deletion):
    auth_data, project_data = create_project_with_deletion
    project_id = project_data['project_id']


    result = success_request_add_token(
        auth_token=auth_data['access_token'],
        project_id=project_id
    )
    print(result)

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_service_token_created'
    )


def test_add_multiple_tokens_success(create_project_with_deletion):
    auth_data, project_data = create_project_with_deletion
    project_id = project_data['project_id']

    tokens_count = 3

    for i in range(tokens_count):
        result = success_request_add_token(
            auth_token=auth_data['access_token'],
            project_id=project_id
        )

        check_rest_response(
            response=result,
            status=ResponseStatus.OK,
            msg_code='push_console_service_token_created'
        )


def test_add_token_unauthorized(create_project_with_deletion):
    _, project_data = create_project_with_deletion
    project_id = project_data['project_id']

    result = unsuccessful_request_add_token(
        auth_token="",
        project_id=project_id,
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )

def test_add_token_invalid_token(create_project_with_deletion, invalid_token):
    _, project_data = create_project_with_deletion
    project_id = project_data['project_id']

    result = unsuccessful_request_add_token(
        auth_token= invalid_token,
        project_id=project_id,
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )


def test_add_token_invalid_project_id(create_authorized_user, invalid_project_id):
    _, auth_data = create_authorized_user

    result = unsuccessful_request_add_token(
        auth_token=auth_data['access_token'],
        project_id=invalid_project_id,
        status_code=404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_project_not_found'
    )

@pytest.mark.skip("Return 500 instead of 422")
def test_add_token_invalid_project_name(create_authorized_user, invalid_project_name):
    _, auth_data = create_authorized_user

    result = unsuccessful_request_add_token(
        auth_token=auth_data['access_token'],
        project_id=invalid_project_name,
        status_code=422
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='go_validation'
    )

