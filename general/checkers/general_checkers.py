
import allure
import pytest
from pydantic import ValidationError

from test_data.enums import ResponseStatus


@allure.step('General check')
def general_checker(actual, expected):
    assert actual == expected, f'Actual result: {actual} vs\Expected result: {expected}'

@allure.step('Check REST response')
def check_rest_response(response, msg_code, status=ResponseStatus.ERROR):
    """
    Проверка полей REST ответа, которые есть всегда.
    :param response:
    :param msg_code:
    :param status:
    :return: None
    """
    general_checker(actual=response['msg_code'], expected=msg_code)
    general_checker(actual=response['status'], expected=status)


@allure.step('Check pydantic model')
def check_pydantic_model(pydantic_model, response: dict):
    try:
        return pydantic_model(**response)
    except ValidationError as error:
        pytest.fail(str(error))
