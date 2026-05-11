import allure
import pytest
from selenium import webdriver
from config import BASE_URL
from pages.registry_page import PageRegistry
from general.utils import rand_project_name, rand_app_name, rand_package_name, rand_app_signature

def test_ui_selenium_create_app_in_project(project_ui):
    driver, pages = project_ui

    with allure.step("Add app to project"):
        pages.projects_page.plus_app_to_project_click()
        pages.projects_page.fill_app_data(rand_app_name(), rand_package_name(), rand_app_signature())
        pages.projects_page.button_create_app_click()

    driver.quit()