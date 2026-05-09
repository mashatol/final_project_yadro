import re

import pytest
from playwright.sync_api import Page
from selenium import webdriver
from config import BASE_URL
from general.utils import rand_project_name
from pages.registry_page import PageRegistry


@pytest.fixture()
def pages(page: Page):
    return PageRegistry(page)

@pytest.fixture()
def auth_user_ui(valid_user_data):
    driver = webdriver.Firefox()
    driver.maximize_window()

    pages = PageRegistry(driver)

    pages.login_page.open(BASE_URL)
    pages.login_page.fill_inputs(valid_user_data)
    pages.login_page.click_submit()
    pages.projects_page.expect_with_projects()

    return driver, pages

@pytest.fixture()
def project_ui(auth_user_ui):
    driver, pages = auth_user_ui

    pages.projects_page.button_plus_click()
    pages.projects_page.name_input_click(rand_project_name())
    pages.projects_page.button_create_click()
    pages.projects_page.expect_with_project_id()

    return driver, pages