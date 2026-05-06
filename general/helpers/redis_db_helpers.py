import allure
from general.clients.redis_db import get_redis_data


@allure.step("Get value key='projects:count:user' by user_id from redis")
def get_projects_count_by_user_id_from_redis(user_id):
    key = f'projects:count:user:{user_id}'

    return get_redis_data(key=key)


@allure.step("Get value key='projects:item' by project_id from redis")
def get_projects_item_by_project_id_from_redis(project_id):
    key = f'projects:item:{project_id}'

    return get_redis_data(key=key)


@allure.step("Get apps count by project_id from redis")
def get_apps_count_by_project_id_from_redis(project_id):
    key = f'apps:count:project:{project_id}'
    return get_redis_data(key=key)

@allure.step("Get apps list by project_id from redis")
def get_apps_list_by_project_id_from_redis(project_id):
    key = f'apps:list:project:{project_id}'
    return get_redis_data(key=key)

@allure.step("Get app item by app_id from redis")
def get_app_item_by_id_from_redis(app_id):
    key = f'apps:item:{app_id}'
    return get_redis_data(key=key)

@allure.step("Get service tokens count by project_id from redis")
def get_service_tokens_count_by_project_id_from_redis(project_id):
    key = f'service_tokens:count:project:{project_id}'
    return get_redis_data(key=key)

@allure.step("Get service tokens list by project_id from redis")
def get_service_tokens_list_by_project_id_from_redis(project_id):
    key = f'service_tokens:list:project:{project_id}'
    return get_redis_data(key=key)

@allure.step("Get app signatures count by app_id from redis")
def get_app_signatures_count_by_app_id_from_redis(app_id):
    key = f'app_signatures:count:app:{app_id}'
    return get_redis_data(key=key)

@allure.step("Get app signatures list by app_id from redis")
def get_app_signatures_list_by_app_id_from_redis(app_id):
    key = f'app_signatures:list:app:{app_id}'
    return get_redis_data(key=key)