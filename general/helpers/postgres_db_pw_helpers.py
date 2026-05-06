import allure

from models.peewee_models.push_console_pw_models import PushConsoleProjectsPW


@allure.step('Get projects by user_id from postgres')
def get_projects_by_user_id_from_postgres_pw(user_id):
    result = list(PushConsoleProjectsPW.select().where(PushConsoleProjectsPW.creator == user_id).dicts())
    return result