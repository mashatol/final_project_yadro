# test_ui_app.py
import allure
import pytest
from selenium import webdriver
from config import BASE_URL
from pages.registry_page import PageRegistry
from general.utils import rand_project_name, rand_app_name, rand_package_name, rand_app_signature

pytest_plugins = [
    'fixtures.ui_fixtures',
    'fixtures.auth_fixtures'
]

def test_ui_selenium_create_app_in_project(valid_user_data):
    driver = webdriver.Firefox()
    driver.maximize_window()

    pages = PageRegistry(driver)

    with allure.step("User open login page"):
        pages.login_page.open(BASE_URL)
        pages.login_page.fill_inputs(valid_user_data)
        pages.login_page.click_submit()

    pages.projects_page.expect_with_projects()

    with allure.step("Create new project"):
        pages.projects_page.button_plus_click()
        pages.projects_page.name_input_click(rand_project_name())
        pages.projects_page.button_create_click()

    # 3. Создание приложения (на той же странице)
    pages.projects_page.plus_app_to_project_click()
    pages.projects_page.fill_app_data(rand_app_name(), rand_package_name(), rand_app_signature())
    pages.projects_page.button_create_app_click()

    driver.quit()