
import allure
import pytest
from selenium import webdriver
from config import BASE_URL
from pages.registry_page import PageRegistry
from general.utils import rand_project_name

pytest_plugins = [
    'fixtures.ui_fixtures',
    'fixtures.auth_fixtures'
]

@allure.step("Test success create project")
def test_ui_selenium_project_valid_credentials(auth_user_ui):
    driver, pages = auth_user_ui

    with allure.step("Create new project"):
        pages.projects_page.button_plus_click()
        pages.projects_page.name_input_click(rand_project_name())
        pages.projects_page.button_create_click()
        pages.projects_page.expect_with_project_id()

    driver.quit()



