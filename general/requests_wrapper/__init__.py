from http import HTTPStatus, HTTPMethod
from json import JSONDecodeError

import allure
import pytest
import requests
from requests import HTTPError

from general.checkers.general_checkers import check_pydantic_model


@allure.step('Make REST request')
def make_rest_request(
        method=HTTPMethod.POST,
        url=None,
        return_only_status=False,
        status_code=HTTPStatus.OK,
        headers=None,
        params=None,
        data=None,
        pydantic_model=None,
        **kwargs
):
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data, **kwargs)
        if return_only_status:
            return response.status_code

        if HTTPStatus.OK <= response.status_code <= HTTPStatus.INTERNAL_SERVER_ERROR and response.status_code == status_code:
            try:
                response = response.json()
            except JSONDecodeError:
                response = response.text

            if pydantic_model:
                check_pydantic_model(pydantic_model=pydantic_model, response=response)

            return response
        else:
            pytest.fail(f'Wrong response status code: real {response.status_code} vs expected {status_code}\n'
                        f'Response text: {response.text}')
    except HTTPError as error:
        raise Exception(f"Something went wrong: {error}")
