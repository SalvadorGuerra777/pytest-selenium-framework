from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, "[data-test='username']")
    PASSWORD = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        return InventoryPage(self.driver)

    def error_message(self):
        return self.text_of(self.ERROR)
