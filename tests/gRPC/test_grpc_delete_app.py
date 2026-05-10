import allure

from general.checkers.general_checkers import general_checker
from general.route.grpc_routes import grpc_delete_app, grpc_delete_app_signature

pytest_plugins = [
    'fixtures.auth_fixtures',
    'fixtures.app_fixtures',
    'fixtures.project_fixtures'
]

@allure.step('Test success delete app')
def test_grpc_delete_app_success(access_token, app_setup_delete):
    result = grpc_delete_app(
        auth_token=access_token,
        project_id=app_setup_delete['project_id'],
        app_id=app_setup_delete['app_id']
    )

    general_checker(actual= 'success' in result, expected= True)

@allure.step('Test unsuccessful delete app with not_found app_id')
def test_grpc_delete_app_not_found(create_project_with_deletion, not_found_app_id):
    auth_data, project_data = create_project_with_deletion
    result = grpc_delete_app(
        auth_token=auth_data['access_token'],
        project_id=project_data['project_id'],
        app_id=not_found_app_id
    )

    general_checker(actual= 'error' in result, expected= True)

@allure.step('Test unsuccessful delete app from project with invalid project_id')
def test_grpc_delete_app_invalid_project_id(access_token, app_setup_delete):
    result = grpc_delete_app(
        auth_token=access_token,
        project_id="not-a-uuid",
        app_id=app_setup_delete['app_id']
    )

    general_checker(actual='error' in result, expected=True)

@allure.step('Test unsuccessful delete app without app_id')
def test_grpc_delete_app_empty_app_id(access_token, create_project_with_deletion):
    auth_data, project_data = create_project_with_deletion

    result = grpc_delete_app(
        auth_token=access_token,
        project_id=project_data['project_id'],
        app_id=" "
    )

    general_checker(actual='error' in result, expected=True)

@allure.step('Test unsuccessful delete app without project_id')
def test_grpc_delete_app_empty_project_id(access_token, app_setup_delete):
    result = grpc_delete_app(
        auth_token=access_token,
        project_id=" ",
        app_id=app_setup_delete['app_id']
    )

    general_checker(actual='error' in result, expected=True)

@allure.step('Test unsuccessful delete already delete app')
def test_grpc_delete_app_already_deleted(access_token, app_setup_delete):
    result1 = grpc_delete_app(
        auth_token=access_token,
        project_id=app_setup_delete['project_id'],
        app_id=app_setup_delete['app_id']
    )
    general_checker(actual='success' in result1, expected=True)

    result2 = grpc_delete_app(
        auth_token=access_token,
        project_id=app_setup_delete['project_id'],
        app_id=app_setup_delete['app_id']
    )
    general_checker(actual='error' in result2, expected=True)