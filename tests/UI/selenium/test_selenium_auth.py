
import allure
from selenium import webdriver

from config import BASE_URL
from pages.login_page import LoginPage
from pages.registry_page import PageRegistry

pytest_plugins = [
    'fixtures.ui_fixtures',
    'fixtures.auth_fixtures'
]

@allure.step("Test success authorization")
def test_ui_selenium_auth_valid_credentials(valid_user_data):
    driver = webdriver.Firefox()
    driver.maximize_window()

    with allure.step("User open login page"):
        pages = PageRegistry(driver)
        pages.login_page.open(BASE_URL)
        pages.login_page.expect_skeleton()

    with allure.step("User enters email and password"):
        pages.login_page.fill_inputs(valid_user_data)
        pages.login_page.expect_filled(valid_user_data)

    with allure.step("User enters email and password"):
        pages.login_page.click_submit()
        pages.projects_page.expect_with_projects()

    driver.quit()