import pytest

from general.checkers.general_checkers import check_rest_response, general_checker
from general.checkers.user_checkers import check_user_data
from general.route.user_routes import \
    unsuccessful_request_approve_user, unsuccessful_request_block_user, unsuccessful_request_promote_user
from test_data.enums import ResponseStatus
from test_data.user_test_data import user_test_data

pytest_plugins = [
    'fixtures.auth_fixtures',
    'fixtures.project_fixtures'
]


def test_unsuccessful_approve_user(create_authorized_user):
    """Обычный пользователь не может approve другого пользователя"""
    _, user_data = create_authorized_user
    _, another_user = create_authorized_user

    result = unsuccessful_request_approve_user(
        auth_token=user_data['access_token'],
        user_id=another_user['user_id']
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_access_denied'
    )

def test_unsuccessful_block_user(create_authorized_user):
    """Обычный пользователь не может block другого пользователя"""
    _, user_data = create_authorized_user
    _, another_user = create_authorized_user

    result = unsuccessful_request_block_user(
        auth_token=user_data['access_token'],
        user_id=another_user['user_id']
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_access_denied'
    )

def test_unsuccessful_promote_user(create_authorized_user):
    """Обычный пользователь не может promote другого пользователя"""
    _, user_data = create_authorized_user
    _, another_user = create_authorized_user

    result = unsuccessful_request_promote_user(
        auth_token=user_data['access_token'],
        user_id=another_user['user_id']
    )

    check_rest_response(
        response=result,
        status=ResponseStatus.ERROR,
        msg_code='general_access_denied'
    )