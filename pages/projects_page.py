# pages/projects_page.py
import re

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from pages.base_page import BasePage

class ProjectsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # locators
    @property
    def projects_title(self):
        return self.driver.find_element(By.XPATH, "//div[@class='header__title']")

    @property
    def button_plus(self):
        return self.driver.find_element(By.CSS_SELECTOR, "app-projects-table div button[appearance='secondary']")

    @property
    def name_input(self):
        return self.driver.find_element(By.CSS_SELECTOR, "div tui-textfield input[data-appearance='textfield']")

    @property
    def button_create(self):
        return self.driver.find_element(By.CSS_SELECTOR, "div button[data-appearance='primary']")

    @property
    def plus_app_to_project(self):
        return self.driver.find_element(By.CSS_SELECTOR, "div div[data-appearance='secondary']")

    @property
    def app_name_input(self):
        return self.driver.find_element(By.CSS_SELECTOR, "div tui-textfield input[formcontrolname = 'name']")

    @property
    def app_package_input(self):
        return self.driver.find_element(By.CSS_SELECTOR,
                                        "div tui-textfield input[formcontrolname = 'package_name']")

    @property
    def app_signature_input(self):
        return self.driver.find_element(By.CSS_SELECTOR,
                                        "div tui-textfield textarea[formcontrolname = 'app_signature']")

    @property
    def button_create_app(self):
        return self.driver.find_element(By.CSS_SELECTOR, "div button[data-appearance='primary']")

    # actions
    def button_plus_click(self):
        self.button_plus.click()

    def name_input_click(self, name):
        self.name_input.click()
        self.name_input.send_keys(name)

    def button_create_click(self):
        ActionChains(self.driver).move_to_element(self.button_create).click().perform()

    def plus_app_to_project_click(self):
        self.plus_app_to_project.click()

    def fill_app_data(self, name_app, package_name, app_signature):
        self.app_name_input.click()
        self.app_name_input.send_keys(name_app)
        self.app_package_input.click()
        self.app_package_input.send_keys(package_name)
        self.app_signature_input.click()
        self.app_signature_input.send_keys(app_signature)

    def button_create_app_click(self):
        self.button_create_app.click()
    #
    #
    # def get_project_id_from_current_url(self):
    #     current_url = self.driver.current_url
    #     match = re.search(r'projects/([a-f0-9-]+)', current_url)
    #     return match.group(1) if match else None


    # expectations
    def expect_with_projects(self):
        self.wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='header__title']")))

    def expect_with_project_id(self):
        self.wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "tui-breadcrumbs a[class = 'ng-star-inserted']")))
