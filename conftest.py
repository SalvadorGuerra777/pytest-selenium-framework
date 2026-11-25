import json
from pathlib import Path

import pytest
from selenium import webdriver

import config
from pages.login_page import LoginPage

SCREENSHOTS = Path("reports/screenshots")


def chrome():
    options = webdriver.ChromeOptions()
    if config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,768")
    # Chrome's leaked-password popup appears with SauceDemo's demo credentials and blocks clicks
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    return webdriver.Chrome(options=options)


def firefox():
    options = webdriver.FirefoxOptions()
    if config.HEADLESS:
        options.add_argument("-headless")
    browser = webdriver.Firefox(options=options)
    browser.set_window_size(1366, 768)
    return browser


BROWSERS = {"chrome": chrome, "firefox": firefox}


@pytest.fixture
def driver():
    if config.BROWSER not in BROWSERS:
        raise pytest.UsageError(f"BROWSER must be one of {sorted(BROWSERS)}, got {config.BROWSER!r}")
    browser = BROWSERS[config.BROWSER]()
    yield browser
    browser.quit()


@pytest.fixture
def inventory(driver):
    login = LoginPage(driver)
    login.open()
    return login.login("standard_user", config.PASSWORD).wait_until_loaded()


@pytest.fixture
def customer():
    return json.loads(Path("data/customer.json").read_text())


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    browser = item.funcargs.get("driver")
    if report.when == "call" and report.failed and browser:
        SCREENSHOTS.mkdir(parents=True, exist_ok=True)
        browser.save_screenshot(str(SCREENSHOTS / f"{item.name}.png"))
        html = item.config.pluginmanager.getplugin("html")
        if html:
            report.extras = getattr(report, "extras", []) + [html.extras.png(browser.get_screenshot_as_base64())]
