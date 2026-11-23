from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE = (By.CSS_SELECTOR, "[data-test='continue']")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    ITEM_TOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TAX = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")
    FINISH = (By.CSS_SELECTOR, "[data-test='finish']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def fill_information(self, first_name, last_name, postal_code):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE)

    def error_message(self):
        return self.text_of(self.ERROR)

    def item_total(self):
        return self.money(self.text_of(self.ITEM_TOTAL))

    def tax(self):
        return self.money(self.text_of(self.TAX))

    def total(self):
        return self.money(self.text_of(self.TOTAL))

    def finish(self):
        self.click(self.FINISH)

    def confirmation(self):
        return self.text_of(self.COMPLETE_HEADER)
