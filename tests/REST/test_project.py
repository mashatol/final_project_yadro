from itertools import count
from types import NoneType
from config import BASE_URL
from general.checkers.general_checkers import general_checker, check_rest_response
from general.checkers.rabbitmq_checkers import check_rabbit_event
from general.clients.rabbitmq import create_rabbit_queue
from general.helpers import add_auth_header_to_default
from general.helpers.postgres_db_helpers import get_project_by_id_from_pg, get_projects_by_user_id_from_pg, \
    get_service_tokens_by_project_id_from_pg, get_service_tokens_count_by_project_id_from_pg
from general.helpers.postgres_db_pw_helpers import get_projects_by_user_id_from_postgres_pw, \
    get_projects_count_by_user_id_from_postgres_pw, get_projects_count_by_project_id_from_postgres_pw
from general.helpers.redis_db_helpers import get_projects_item_by_project_id_from_redis, \
    get_projects_count_by_user_id_from_redis, get_service_tokens_count_by_project_id_from_redis
from general.requests_wrapper import make_rest_request
from general.route.project_routes import success_request_update_project, \
    unsuccessful_request_update_project, \
    success_request_delete_project, unsuccessful_request_delete_project, PROJECTS_ID_ROUTE, success_request_add_token, \
    unsuccessful_request_add_token, success_request_get_projects, unsuccessful_request_delete_token, \
    success_request_delete_token
from general.utils import rand_project_name
from test_data.enums import ResponseStatus
import pytest

pytest_plugins = [
    'fixtures.auth_fixtures',
    'fixtures.project_fixtures'
]

def test_successful_get_projects(create_project_with_deletion):
    auth_data, project_data = create_project_with_deletion

    db_data = get_projects_by_user_id_from_pg(user_id=auth_data['user_id'])

    result = success_request_get_projects(auth_token=auth_data['access_token'])
    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_projects_successful_getting'
    )

    redis_projects_count = get_projects_count_by_user_id_from_redis(user_id=auth_data['user_id'])

    print(len(db_data))
    print(redis_projects_count)
    print(result['_meta']['total_count'])

def test_delete_project_success(create_project):
    auth_data, project = create_project

    queue_name = create_rabbit_queue(exchange='test_course', routing_key='sync')

    db_pw_before = get_projects_count_by_project_id_from_postgres_pw(project['data']['project_id'])
    general_checker(actual= db_pw_before > 0, expected=True)

    db_before = get_project_by_id_from_pg(project_id=project['data']['project_id'])
    general_checker(actual=len(db_before) > 0, expected=True)

    result = success_request_delete_project(auth_token=auth_data['access_token'],
                                            project_id=project['data']['project_id'])
    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_project_successful_deleted'
    )
    check_rabbit_event(queue_name=queue_name, expected_event_type='push-console_sync.projects.remove')

    db_pw_after = get_projects_count_by_project_id_from_postgres_pw(project['data']['project_id'])
    general_checker(actual=db_pw_after, expected= 0)

    db_after = get_project_by_id_from_pg(project_id=project['data']['project_id'])
    general_checker(actual=len(db_after), expected=0)

def test_delete_project_invalid_id(create_project, invalid_project_id):
    auth_data, project = create_project

    db_projects_before = get_project_by_id_from_pg(auth_data['user_id'])
    count_before = len(db_projects_before)

    result = unsuccessful_request_delete_project(auth_token=auth_data['access_token'],
                                                 status_code = 404,
                                                project_id=invalid_project_id)
    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_project_not_found'
    )
    db_projects_after = get_project_by_id_from_pg(auth_data['user_id'])
    general_checker(actual=len(db_projects_after), expected=count_before)

def test_delete_project_unauthorized(create_project):
    auth_data, project = create_project

    db_projects_before = get_project_by_id_from_pg(auth_data['user_id'])
    count_before = len(db_projects_before)

    result = unsuccessful_request_delete_project(
        auth_token="",
        project_id=project['data']['project_id'],
        status_code = 401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )

    db_projects_after = get_project_by_id_from_pg(auth_data['user_id'])
    general_checker(actual=len(db_projects_after), expected=count_before)

def test_delete_project_invalid_token(create_project, invalid_token):
    auth_data, project = create_project

    db_projects_before = get_project_by_id_from_pg(auth_data['user_id'])
    count_before = len(db_projects_before)

    result = unsuccessful_request_delete_project(
        auth_token=invalid_token,
        project_id=project['data']['project_id'],
        status_code = 401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )

    db_projects_after = get_project_by_id_from_pg(auth_data['user_id'])
    general_checker(actual=len(db_projects_after), expected=count_before)


def test_delete_already_deleted_project(create_project):
    auth_data, project = create_project

    success_request_delete_project(
        auth_token=auth_data['access_token'],
        project_id=project['data']['project_id']
    )

    db_projects_before = get_project_by_id_from_pg(auth_data['user_id'])
    count_before = len(db_projects_before)

    result = unsuccessful_request_delete_project(
        auth_token=auth_data['access_token'],
        project_id=project['data']['project_id'],
        status_code = 404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_project_not_found'
    )

    db_projects_after = get_project_by_id_from_pg(auth_data['user_id'])
    general_checker(actual=len(db_projects_after), expected=count_before)

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

    db_project_before = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_before['name'], expected=update_project_data['old_name'])

    result = unsuccessful_request_update_project(
        auth_token="",
        request_body={"name": rand_project_name()},
        project_id=update_project_data['project_id'],
        status_code=401
    )

    check_rest_response(response=result,
                        status=ResponseStatus.ERROR,
                        msg_code='general_unauthorized')

    db_project_after = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_after['name'], expected=update_project_data['old_name'])


def test_update_project_invalid_token(update_project_data, invalid_token):

    db_project_before = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_before['name'], expected=update_project_data['old_name'])

    result = unsuccessful_request_update_project(
        auth_token=invalid_token,
        request_body={"name": rand_project_name()},
        project_id=update_project_data['project_id'],
        status_code=401
    )

    check_rest_response(response=result,
                        status=ResponseStatus.ERROR,
                        msg_code='general_bad_token')
    db_project_after = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_after['name'], expected=update_project_data['old_name'])


def test_update_project_invalid_id(update_project_data, invalid_project_id):

    db_project_before = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_before['name'], expected=update_project_data['old_name'])

    result = unsuccessful_request_update_project(
        auth_token=update_project_data['auth_token'],
        request_body={"name": rand_project_name()},
        project_id=invalid_project_id,
        status_code=404
    )

    check_rest_response(response=result,
                        status=ResponseStatus.ERROR,
                        msg_code='push_console_project_not_found')

    db_project_after = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_after['name'], expected=update_project_data['old_name'])


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

    db_project_after = get_project_by_id_from_pg(update_project_data['project_id'])[0]
    general_checker(actual=db_project_after['name'], expected=update_project_data['old_name'])


def test_add_service_token_success(create_project_with_deletion):
    auth_data, project_data = create_project_with_deletion

    queue_name = create_rabbit_queue(exchange='test_course', routing_key='sync')

    db_pw_before = get_service_tokens_count_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual=db_pw_before==0, expected=True)

    db_before = get_service_tokens_count_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual = db_before==0, expected=True)

    result = success_request_add_token(
        auth_token=auth_data['access_token'],
        project_id=project_data['project_id']
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_service_token_created'
    )

    check_rabbit_event(queue_name=queue_name, expected_event_type='push-console_sync.tokens.create')

    db_pw_after = get_service_tokens_count_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual=db_pw_after is not None, expected=True)

    db_after = get_service_tokens_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual=db_after is not None, expected=True)


def test_add_multiple_tokens_success(create_project_with_deletion):
    auth_data, project_data = create_project_with_deletion

    queue_name = create_rabbit_queue(exchange='test_course', routing_key='sync')

    db_before = get_service_tokens_count_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual=db_before==0, expected=True)

    tokens_count = 3

    for i in range(tokens_count):
        result = success_request_add_token(
            auth_token=auth_data['access_token'],
            project_id=project_data['project_id']
        )

        check_rest_response(
            response=result,
            status=ResponseStatus.OK,
            msg_code='push_console_service_token_created'
        )

    check_rabbit_event(queue_name=queue_name, expected_event_type='push-console_sync.tokens.create')

    db_after = get_service_tokens_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual=len(db_after), expected=tokens_count)



def test_add_token_unauthorized(create_project_with_deletion):
    _, project_data = create_project_with_deletion

    db_before = get_service_tokens_count_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual=db_before==0, expected=True)

    result = unsuccessful_request_add_token(
        auth_token="",
        project_id=project_data['project_id'],
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_unauthorized'
    )

    db_after = get_service_tokens_count_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual=db_before, expected=db_after)

def test_add_token_invalid_token(create_project_with_deletion, invalid_token):
    _, project_data = create_project_with_deletion

    db_before = get_service_tokens_count_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual=db_before== 0, expected=True)

    result = unsuccessful_request_add_token(
        auth_token= invalid_token,
        project_id=project_data['project_id'],
        status_code=401
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_bad_token'
    )

    db_after = get_service_tokens_count_by_project_id_from_pg(project_data['project_id'])
    general_checker(actual=db_before, expected=db_after)


def test_add_token_invalid_project_id(create_authorized_user, invalid_project_id):
    _, auth_data = create_authorized_user

    db_before = get_service_tokens_count_by_project_id_from_pg(invalid_project_id)
    general_checker(actual=db_before==0, expected=True)

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

    db_after = get_service_tokens_count_by_project_id_from_pg(invalid_project_id)
    general_checker(actual=db_before, expected=db_after)

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

def test_delete_service_token_success(create_service_token_to_delete):

    db_pw_before = get_service_tokens_count_by_project_id_from_pg(create_service_token_to_delete['project_id'])
    general_checker(actual=db_pw_before is not None, expected=True)

    result = success_request_delete_token(
        auth_token=create_service_token_to_delete['auth_token'],
        project_id=create_service_token_to_delete['project_id'],
        token_value=create_service_token_to_delete['token_value']
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.OK,
        msg_code='push_console_service_token_deleted'
    )

    db_pw_after = get_service_tokens_count_by_project_id_from_pg(create_service_token_to_delete['project_id'])
    general_checker(actual=db_pw_after==0, expected=True)

@pytest.mark.skip("Return 200 instead of 404")
def test_delete_service_token_invalid_value(create_project_with_deletion):
    auth_data, project_data = create_project_with_deletion
    invalid_token_value = "123!@#"

    result = unsuccessful_request_delete_token(
        auth_token=auth_data['access_token'],
        project_id=project_data['project_id'],
        token_value=invalid_token_value,
        status_code=404
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='push_console_service_token_not_found'
    )



