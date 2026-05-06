
class LoginTestData:
    go_validation_msg_code = 'go_validation'
    push_console_bad_credentials = 'push_console_bad_credentials'


    # Negative messages
    @staticmethod
    def invalid_data_type_message(param, field):
        type_ = None
        if isinstance(param, bool):
            type_ = 'bool'
        elif isinstance(param, int) or isinstance(param, float):
            type_ = 'number'
        elif isinstance(param, list) or isinstance(param, tuple):
            type_ = 'array'
        else:
            type_ = 'object'
        return f"error with parsing body: json: cannot unmarshal {type_} into Go struct field UserLoginPresenter.{field} of type string"


login_test_data = LoginTestData()