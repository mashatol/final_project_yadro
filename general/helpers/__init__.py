import allure
@allure.step('Add authorization token to default headers')
def add_auth_header_to_default(auth_token, default_headers=None):
    headers = default_headers if default_headers is not None else {}
    headers.update({'Authorization': f'Bearer {auth_token}'})
    return headers