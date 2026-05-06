import pytest
from faker import Faker
from config import EMAIL, PASSWORD
from general.route.auth_routes import success_request_login_user, success_request_logout_user
from general.utils import random_email, random_password, rand_str
from test_data.auth_test_data import login_test_data
fake = Faker()

@pytest.fixture()
def random_user_data():
    return {
        "email": random_email(),
        "password": random_password()
    }


@pytest.fixture()
def valid_user_data():
    return {
        "email": EMAIL,
        "password": PASSWORD
    }

@pytest.fixture(params=['email', 'password'])
def user_data_no_email_or_password(request, valid_user_data):
    user_data = valid_user_data
    del user_data[request.param]

    return user_data

@pytest.fixture(params=[('email', 422, login_test_data.go_validation_msg_code), ('password', 409, login_test_data.push_console_bad_credentials)
])
def user_data_incorrect_email_or_password(request, valid_user_data):
    field_to_delete, status_code, msg_code = request.param
    user_data=valid_user_data.copy()
    user_data[field_to_delete]=rand_str()
    return {
        'field' : field_to_delete,
        'body' : user_data,
        'status_code': status_code,
        'msg_code': msg_code
    }


@pytest.fixture(params=[
    ('email', 1),
    ('email', 1.1),
    ('email', True),
    ('email', []),
    ('email', ()),
    ('email', {}),
    ('password', 1),
    ('password', 1.1),
    ('password', True),
    ('password', []),
    ('password', ()),
    ('password', {}),
])
def invalid_data_type(request, valid_user_data):
    field_to_change, invalid_data_type = request.param

    user_data = valid_user_data.copy()
    user_data[field_to_change] = invalid_data_type

    expected_reason = login_test_data.invalid_data_type_message(invalid_data_type, field_to_change)

    return {
        'body': user_data,
        'expected_reason': expected_reason,
        'field': field_to_change,
        'invalid_data_type': invalid_data_type
    }


@pytest.fixture()
def access_token():
    response = success_request_login_user()
    access_token = response['data']['access_token']
    return access_token

@pytest.fixture()
def refresh_token():
    response = success_request_login_user()
    refresh_token = response['data']['refresh_token']
    return refresh_token

@pytest.fixture()
def user_id():
    response = success_request_login_user()
    user_id = response['data']['user_id']
    return user_id

@pytest.fixture()
def valid_change_password_body(valid_user_data):
    return {
        "old_password": valid_user_data["password"],
        "new_password": "MashaLol123!"
    }

@pytest.fixture(params = ['old_password', 'new_password'])
def change_password_no_old_or_new_password(request,valid_change_password_body):
    change_password_body = valid_change_password_body
    del change_password_body[request.param]
    return change_password_body

@pytest.fixture()
def create_authorized_user(valid_user_data):
    request_body = valid_user_data
    response = success_request_login_user()

    yield request_body['email'], response['data']

    success_request_logout_user(auth_token=response['data']['access_token'])

@pytest.fixture(params=[
    ('old_password', 123),
    ('old_password', 1.1),
    ('old_password', True),
    ('old_password', None),
    ('old_password', []),
    ('old_password', {}),
    ('new_password', 123),
    ('new_password', 1.1),
    ('new_password', True),
    ('new_password', None),
    ('new_password', []),
    ('new_password', {}),
])
def invalid_password_type(request, valid_change_password_body):
    """Невалидные типы для полей пароля"""
    field, value = request.param
    body = valid_change_password_body.copy()
    body[field] = value
    return body

@pytest.fixture(params=[
    "token with spaces",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.malformed",
    None,
    123,
    True,
])
def invalid_token(request):
    return request.param