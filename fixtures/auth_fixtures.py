import pytest
from config import EMAIL, PASSWORD
from general.route.auth_routes import success_request_login_user, success_request_logout_user

@pytest.fixture()
def valid_user_data():
    return {
        "email": EMAIL,
        "password": PASSWORD
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

@pytest.fixture(params = ['123',"strstr", None, "CFTYUJNbvfghjnmncdfghjkm.dgfhdj", "mlem-mlem"])
def invalid_refresh_token(request):
    return request.param


@pytest.fixture()
def user_id():
    response = success_request_login_user()
    user_id = response['data']['user_id']
    return user_id

@pytest.fixture()
def valid_change_password_body(valid_user_data):
    return {
        "old_password": valid_user_data["password"],
        "new_password": "Mlemmim123!"
    }

@pytest.fixture()
def create_authorized_user(valid_user_data):
    request_body = valid_user_data
    response = success_request_login_user()

    yield request_body['email'], response['data']

    success_request_logout_user(auth_token=response['data']['access_token'])


@pytest.fixture(params=[
    "token with spaces",
    "eyJhbGciOiJIUzI1NiIsInDGju869CJ9.fgghjl",
    None,
    123,
    True,
])
def invalid_access_token(request):
    return request.param


