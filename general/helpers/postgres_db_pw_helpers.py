import allure

from models.peewee_models.push_console_pw_models import PushConsoleProjectsPW, PushConsoleAppsPW, PushConsoleTokensPW


@allure.step('Get projects by user_id from postgres')
def get_projects_by_user_id_from_postgres_pw(user_id):
    result = list(PushConsoleProjectsPW.select().where(PushConsoleProjectsPW.creator == user_id).dicts())
    return result

@allure.step('Get projects count by user_id from postgres')
def get_projects_count_by_user_id_from_postgres_pw(user_id):
    count = PushConsoleProjectsPW.select().where(PushConsoleProjectsPW.creator == user_id).count()
    return count

@allure.step('Get projects count by project_id from postgres')
def get_projects_count_by_project_id_from_postgres_pw(project_id):
    count = PushConsoleProjectsPW.select().where(PushConsoleProjectsPW.project_id == project_id).count()
    return count

@allure.step('Get app by id from postgres (Peewee)')
def get_app_by_id_from_postgres_pw(app_id):
    result = list(PushConsoleAppsPW.select().where(PushConsoleAppsPW.app_id == app_id).dicts())
    return result

@allure.step('Get apps by project_id from postgres')
def get_apps_by_project_id_from_postgres_pw(project_id):
    result = list(PushConsoleAppsPW.select().where(PushConsoleAppsPW.project == project_id).dicts())
    return result

@allure.step('Get apps count by project_id from postgres')
def get_apps_count_by_project_id_from_postgres_pw(project_id):
    count = PushConsoleAppsPW.select().where(PushConsoleAppsPW.project == project_id).count()
    return count

@allure.step('Get app by name from postgres')
def get_app_by_name_from_pw(app_name):
    result = list(PushConsoleAppsPW.select().where(PushConsoleAppsPW.name == app_name).dicts())
    return result

@allure.step('Get app by package_name from postgres')
def get_app_by_package_name_from_pw(package_name):
    result = list(PushConsoleAppsPW.select().where(PushConsoleAppsPW.package_name == package_name).dicts())
    return result

@allure.step('Get service_tokens by project_id from postgres')
def get_service_tokens_by_project_id_from_pw(project_id):
    result = list(PushConsoleTokensPW.select().where(PushConsoleTokensPW.project == project_id).dicts())
    return result

@allure.step('Get service_tokens count by project_id from postgres')
def get_service_tokens_count_by_project_id_from_pw(project_id):
    count = PushConsoleTokensPW.select().where(PushConsoleTokensPW.project == project_id).count()
    return count
