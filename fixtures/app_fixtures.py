import pytest

from general.route.app_routes import success_request_create_app, success_request_delete_app, success_request_get_apps
from general.utils import rand_app_name, rand_package_name, rand_app_signature



@pytest.fixture
def valid_app_body():
    return {
        "name": rand_app_name(),
        "package_name": rand_package_name(),
        "app_signature": rand_app_signature()
    }


@pytest.fixture(params = ["  ", None,])
def invalid_app_name(request):
    return request.param

@pytest.fixture
def invalid_app_name_body(invalid_app_name):
    return {
        "name": invalid_app_name,
        "package_name": rand_package_name(),
        "app_signature": rand_app_signature()
    }

@pytest.fixture
def invalid_app_signature_body(invalid_app_signature):
    return {
        "name": rand_app_name(),
        "package_name": rand_package_name(),
        "app_signature": invalid_app_signature
    }

@pytest.fixture(params=["",None,"a" * 1000,123,True,{},[]])
def invalid_app_signature(request):
    return request.param


@pytest.fixture(params=["00000000000000000000-0000000000000", "123","True","123456789iujhgfdxz","1q2wesdfgvhvbcxsa"])
def not_found_app_id(request):
    return request.param

@pytest.fixture(params=[
    ['name'],
    ['package_name'],
    ['app_signature'],
    ['name','package_name'],
    ['name', 'app_signature'],
    ['package_name', 'app_signature'],
    ['name', 'package_name', 'app_signature'],
])
def missing_fields(request, valid_app_body):
    missing_fields_list = request.param

    request_body = valid_app_body.copy()
    for field in missing_fields_list:
        if field in request_body:
            del request_body[field]

    return request_body

@pytest.fixture
def create_app(create_project_with_deletion, valid_app_body):
    auth_data, project_data = create_project_with_deletion
    project_id = project_data['project_id']

    create_response = success_request_create_app(
        auth_token=auth_data['access_token'],
        project_id=project_id,
        request_body=valid_app_body
    )

    apps_response = success_request_get_apps(
        auth_token=auth_data['access_token'],
        project_id=project_id,
        pydantic_model=None
    )

    app_id = None
    for app in apps_response['data']:
        if app['name'] == valid_app_body['name']:
            app_id = app['id']
            break

    app_data = {
        'app_id': app_id,
        'app_name': valid_app_body['name'],
        'package_name': valid_app_body['package_name'],
        'app_signature': valid_app_body['app_signature']
    }

    yield auth_data, project_data, create_response, app_data

    if app_id:
        success_request_delete_app(
            auth_token=auth_data['access_token'],
            project_id=project_id,
            app_id=app_id
        )

@pytest.fixture
def app_setup(create_app):
    auth_data, project_data, create_response, app_data = create_app
    return{
        'token': auth_data['access_token'],
        'project_id': project_data['project_id'],
        'app_id': app_data['app_id'],
        'app_name': app_data['app_name']
    }

@pytest.fixture
def valid_update_body():
    return {
        'name': rand_app_name()
    }

@pytest.fixture
def invalid_update_body(invalid_app_name):
    return {
        'name': invalid_app_name
    }

@pytest.fixture
def create_app_without_deletion(create_project_with_deletion, valid_app_body):
    auth_data, project_data = create_project_with_deletion
    project_id = project_data['project_id']

    create_response = success_request_create_app(
        auth_token=auth_data['access_token'],
        project_id=project_id,
        request_body=valid_app_body
    )

    apps_response = success_request_get_apps(
        auth_token=auth_data['access_token'],
        project_id=project_id,
        pydantic_model=None
    )

    app_id = None
    for app in apps_response['data']:
        if app['name'] == valid_app_body['name']:
            app_id = app['id']
            break

    app_data = {
        'app_id': app_id,
        'app_name': valid_app_body['name'],
        'package_name': valid_app_body['package_name'],
        'app_signature': valid_app_body['app_signature']
    }

    yield auth_data, project_data, create_response, app_data

@pytest.fixture
def app_setup_delete(create_app_without_deletion):
    auth_data, project_data, create_response, app_data = create_app_without_deletion
    return{
        'token': auth_data['access_token'],
        'project_id': project_data['project_id'],
        'app_id': app_data['app_id'],
        'app_name': app_data['app_name']
    }
