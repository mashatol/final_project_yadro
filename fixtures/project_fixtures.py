import uuid


from general.helpers.postgres_db_helpers import get_service_tokens_by_project_id_from_pg
from general.route.project_routes import success_request_delete_project, success_request_add_token
from general.utils import rand_project_name
import pytest
from general.utils import rand_str
from general.route.project_routes import success_request_create_project
from test_data.project_test_data import project_test_data




@pytest.fixture()
def create_project(create_authorized_user):
    _, auth_data = create_authorized_user

    request_body = project_test_data.create_project_data(name=rand_str())
    response = success_request_create_project(auth_token=auth_data['access_token'],
                                              request_body=request_body)

    return auth_data, response

@pytest.fixture()
def create_project_with_deletion(create_authorized_user):
    _, auth_data = create_authorized_user

    project_name = rand_project_name()
    request_body = {"name": project_name}

    response = success_request_create_project(auth_token=auth_data['access_token'],
                                              request_body=request_body)

    project_data = {
        'project_id': response ['data']['project_id'],
        'name': project_name
    }

    yield auth_data, project_data

    try:
        success_request_delete_project(
            auth_token=auth_data['access_token'],
            project_id=response['data']['project_id']
        )
    except:
        pass


@pytest.fixture(params=['abc' , None, "", "  "])
def invalid_project_name(request):
    return request.param

@pytest.fixture()
def no_project_name():
    return {
        "name": " "
    }

@pytest.fixture()
def invalid_project_id():
    return str(uuid.uuid4())

@pytest.fixture()
def update_project_data(create_project_with_deletion):
    auth_data, project = create_project_with_deletion
    return {
        'auth_token': auth_data['access_token'],
        'project_id': project['project_id'],
        'old_name': project['name']
    }

@pytest.fixture
def create_service_token_to_delete(create_project_with_deletion):
    auth_data, project_data = create_project_with_deletion
    project_id = project_data['project_id']

    success_request_add_token(
        auth_token=auth_data['access_token'],
        project_id=project_id
    )

    tokens = get_service_tokens_by_project_id_from_pg(project_id)
    value = tokens[0]['value'] if tokens else None

    return {
        'auth_token': auth_data['access_token'],
        'project_id': project_id,
        'token_value': value
    }


