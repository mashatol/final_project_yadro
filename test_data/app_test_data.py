from general.utils import rand_str, convert_to_sha256

class AppTestData:
    @staticmethod
    def app_create_data(name=None, package_name=None, app_signature=None):
        return {
            "name": name if name is not None else rand_str(25),
            "package_name": package_name if package_name is not None else f'{rand_str(10)}.{rand_str(10)}.{rand_str(10)}',
            "app_signature": app_signature if app_signature is not None else convert_to_sha256(rand_str(25))
        }
app_test_data = AppTestData()
