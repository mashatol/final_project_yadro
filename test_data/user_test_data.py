from copy import deepcopy

from test_data.enums import UserQueryParam


class UserTestData:
    """Класс для хранения тестовых данных для эндпоинтов из блока User."""

    push_console_getting_users_successful = 'push_console_getting_users_successful'

    @staticmethod
    def user_query_param(user_role):
        return deepcopy({
            UserQueryParam.ROLE: user_role
        })


user_test_data = UserTestData()
