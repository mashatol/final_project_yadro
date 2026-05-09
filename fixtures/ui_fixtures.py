import pytest
from playwright.sync_api import Page

from pages.registry_page import PageRegistry


@pytest.fixture()
def pages(page: Page):
    return PageRegistry(page)
