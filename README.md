# pytest-selenium-framework

![UI tests](https://github.com/SalvadorGuerra777/pytest-selenium-framework/actions/workflows/ui-tests.yml/badge.svg)

UI test automation framework for [SauceDemo](https://www.saucedemo.com), a public demo store built for practicing test automation. It covers login, product listing, cart and checkout with Python, PyTest and Selenium WebDriver, using the Page Object Model.

## Tech stack

- Python 3.12+
- PyTest, pytest-html (reports), pytest-xdist (parallel runs)
- Selenium WebDriver 4 (Chrome and Firefox, drivers resolved by Selenium Manager)
- GitHub Actions

## Project structure

```
├── pages/                 # Page objects: locators and actions per page
│   ├── base_page.py       # Explicit waits and shared helpers
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                 # Test cases grouped by feature
├── data/customer.json     # Checkout test data
├── conftest.py            # Driver, login and data fixtures, screenshot on failure
├── config.py              # Settings read from environment variables
├── pytest.ini
└── .github/workflows/ui-tests.yml
```

## Setup

```bash
git clone https://github.com/SalvadorGuerra777/pytest-selenium-framework.git
cd pytest-selenium-framework
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Google Chrome or Mozilla Firefox must be installed.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://www.saucedemo.com` | Application under test |
| `BROWSER` | `chrome` | `chrome` or `firefox` |
| `HEADLESS` | `true` | Set to `false` to watch the browser |
| `TIMEOUT` | `10` | Explicit wait timeout in seconds |
| `SAUCE_PASSWORD` | `secret_sauce` | Password for the demo users (published on the SauceDemo login page) |

## Running the tests

```bash
pytest                    # full suite
pytest -n 4               # parallel, 4 workers
pytest -m smoke           # critical paths only
HEADLESS=false pytest tests/test_login.py
```

An HTML report is written to `reports/report.html`. When a test fails, a screenshot is saved in `reports/screenshots/` and embedded in the report. In CI the `reports/` folder is uploaded as the `test-report` artifact.

## What is covered

20 test cases:

| Area | Checks |
|---|---|
| Login | Valid login; locked-out user, wrong password, empty username and empty password (negative cases); direct access to the inventory without logging in |
| Inventory | Six products listed, prices are positive, sorting A-Z, Z-A, price low-high and high-low |
| Cart | Empty cart on login, cart badge and contents after adding items, removing an item |
| Checkout | Full purchase, item total and tax add up to the total, each required customer field is validated |

Last local run: `20 passed` on Chrome and on Firefox with `pytest -n 4` (Windows, headless). CI runs the suite once per browser.

## Design decisions

- Locators use the `data-test` attributes the app provides, which are more stable than CSS classes or text.
- Every interaction goes through explicit waits in `BasePage`; there are no fixed sleeps.
- Each test gets a fresh browser, so tests are independent and can run in parallel.
- Running on Firefox found a timing bug that Chrome hid: the inventory test sometimes counted 0 products because `find_all` read the list before it rendered. The `inventory` fixture now waits for the first product before returning the page. `find_all` itself doesn't wait, because an empty result is valid in some places (no cart badge).
- Negative and boundary cases are parametrized to keep one test function per rule.
