# pages/page_registry.py

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage

class PageRegistry:
    def __init__(self, driver):
        self.driver = driver

    @property
    def login_page(self):
        return LoginPage(self.driver)

    @property
    def projects_page(self):
        return ProjectsPage(self.driver)