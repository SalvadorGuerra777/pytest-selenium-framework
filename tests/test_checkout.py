import pytest

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
def test_complete_purchase(inventory, customer):
    inventory.add_to_cart(BACKPACK)
    checkout = inventory.open_cart().checkout()
    checkout.fill_information(**customer)
    checkout.finish()
    assert checkout.confirmation() == "Thank you for your order!"


def test_order_totals_add_up(inventory, customer):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    cart = inventory.open_cart()
    expected_item_total = sum(cart.item_prices())
    checkout = cart.checkout()
    checkout.fill_information(**customer)
    assert checkout.item_total() == pytest.approx(expected_item_total)
    assert checkout.total() == pytest.approx(checkout.item_total() + checkout.tax())


@pytest.mark.parametrize(
    "missing_field, expected_error",
    [
        ("first_name", "Error: First Name is required"),
        ("last_name", "Error: Last Name is required"),
        ("postal_code", "Error: Postal Code is required"),
    ],
)
def test_checkout_requires_customer_information(inventory, customer, missing_field, expected_error):
    inventory.add_to_cart(BACKPACK)
    checkout = inventory.open_cart().checkout()
    checkout.fill_information(**{**customer, missing_field: ""})
    assert checkout.error_message() == expected_error
