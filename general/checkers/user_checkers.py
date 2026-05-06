import allure

from general.checkers.general_checkers import general_checker


@allure.step('Check user data')
def check_user_data(response: dict, data_from_db: dict):
    """
    :param response:
    :param data_from_db:
    :return: None
    """
    general_checker(actual=response['company_name'], expected=data_from_db['company_name'])
    general_checker(actual=response['id'], expected=data_from_db['id'])
    general_checker(actual=response['email'], expected=data_from_db['email'])
    general_checker(actual=response['created_at'], expected=data_from_db['created_at'])
    general_checker(actual=response['role'], expected=data_from_db['role'])