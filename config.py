import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com").rstrip("/")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
TIMEOUT = int(os.getenv("TIMEOUT", "10"))
# SauceDemo publishes this password on its login page; override it if the target changes
PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
