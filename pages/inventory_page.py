from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")

    def wait_until_loaded(self):
        # find_all doesn't wait, so wait for the first product before reading the list
        self.find(self.ITEM_NAMES)
        return self

    def title(self):
        return self.text_of(self.TITLE)

    def product_names(self):
        return [item.text for item in self.find_all(self.ITEM_NAMES)]

    def product_prices(self):
        return [self.money(price.text) for price in self.find_all(self.ITEM_PRICES)]

    def sort_by(self, option):
        Select(self.find(self.SORT)).select_by_value(option)

    def _item_button(self, name):
        return (By.XPATH, f"//div[@data-test='inventory-item'][.//div[text()='{name}']]//button")

    def add_to_cart(self, name):
        self.click(self._item_button(name))

    # the same button switches between "Add to cart" and "Remove"
    remove_from_cart = add_to_cart

    def cart_count(self):
        badge = self.find_all(self.CART_BADGE)
        return int(badge[0].text) if badge else 0

    def open_cart(self):
        self.click(self.CART_LINK)
        return CartPage(self.driver)
