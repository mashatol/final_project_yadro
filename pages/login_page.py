from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # locators
    @property
    def email_input(self):
        self.wait.until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[formcontrolname='email']")))
        return (self.driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='email']"))

    @property
    def password_input(self):
        self.wait.until(expected_conditions.visibility_of_element_located(
            (By.XPATH, "//input[@formcontrolname='password']")))
        return self.driver.find_element(By.XPATH, "//input[@formcontrolname='password']")

    @property
    def submit_button(self):
        self.wait.until(expected_conditions.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")))
        return self.driver.find_element(By.XPATH, "//button[@type='submit']")

    # actions
    def fill_inputs(self, user_data):
        self.email_input.click()
        self.email_input.send_keys(user_data["email"])
        self.password_input.click()
        self.password_input.send_keys(user_data["password"])

    def click_submit(self):
        self.submit_button.click()

    # expectations
    def expect_skeleton(self):
        self.wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='email']")))
        self.wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='password']")))
        self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

    def expect_filled(self, user_data):
        assert self.email_input.get_attribute("value") == user_data["email"]
        assert self.password_input.get_attribute("value") == user_data["password"]
        assert self.submit_button.is_enabled()