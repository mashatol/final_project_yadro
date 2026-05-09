import hashlib
import random
import string
import allure
from google.protobuf.json_format import MessageToDict


def rand_int(from_=0, to_ =10):
    """
    Generate random int number
    :param from_: start
    :param to_: end
    :return int number
    """
    return random.randint(a=from_, b= to_)

def rand_str(n=10):
    """
    :param n:
    :return:
    """
    required_uppercase = random.choice(string.ascii_uppercase)
    required_lower_case = random.choice(string.ascii_lowercase)
    required_digit = random.choice(string.digits)

    return ''.join([required_uppercase + required_lower_case + required_digit] + random.choices(string.ascii_lowercase, k=n))

def convert_to_sha256(app_signature):
    """
    """
    encoded_str = app_signature.encode('utf-8')
    hashed_str = hashlib.sha256(encoded_str)
    hex_digest = hashed_str.hexdigest()
    return hex_digest

def random_project_id(response):
    projects = response.get('data', [])
    return random.choice(projects)['project_id']


def random_email():
    return f'{rand_str()}@{rand_str()}.com'

def random_password():
    return f'{rand_str()}{string.punctuation}'


@allure.step('Convert proto msg to dict')
def grpc_msg_to_dict(grpc_msg):
    return MessageToDict(grpc_msg)

@allure.step('Create random project name')
def rand_project_name():
    name = f"{rand_str()}_{random.randint(1 , 999)}"
    if len(name) > 50:
        name = name[:50]
    return name

@allure.step('Create valid random app name')
def rand_app_name():
    length = random.randint(5, 50)
    chars = string.ascii_letters + string.digits + '_-'
    return ''.join(random.choice(chars) for _ in range(length))

@allure.step('Create valid random package_name')
def rand_package_name():
    return f"com.example.{rand_str()}_{random.randint(1, 9999)}"

@allure.step('Create valid random app_signature')
def rand_app_signature():
    return ''.join(random.choices(string.hexdigits, k=64))