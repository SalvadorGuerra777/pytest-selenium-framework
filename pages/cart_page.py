from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    CHECKOUT = (By.CSS_SELECTOR, "[data-test='checkout']")

    def item_names(self):
        return [item.text for item in self.find_all(self.ITEM_NAMES)]

    def item_prices(self):
        return [self.money(price.text) for price in self.find_all(self.ITEM_PRICES)]

    def checkout(self):
        self.click(self.CHECKOUT)
        return CheckoutPage(self.driver)
