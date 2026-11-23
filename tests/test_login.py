import pytest

import config
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_standard_user_can_log_in(driver):
    login = LoginPage(driver)
    login.open()
    inventory = login.login("standard_user", config.PASSWORD)
    assert inventory.title() == "Products"


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", config.PASSWORD, "Epic sadface: Sorry, this user has been locked out."),
        ("standard_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
        ("", config.PASSWORD, "Epic sadface: Username is required"),
        ("standard_user", "", "Epic sadface: Password is required"),
    ],
    ids=["locked_out_user", "wrong_password", "empty_username", "empty_password"],
)
def test_login_shows_error(driver, username, password, expected_error):
    login = LoginPage(driver)
    login.open()
    login.login(username, password)
    assert login.error_message() == expected_error


def test_inventory_is_blocked_without_login(driver):
    login = LoginPage(driver)
    login.open("inventory.html")
    assert "You can only access '/inventory.html' when you are logged in" in login.error_message()
