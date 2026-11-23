import pytest


def test_inventory_lists_six_products(inventory):
    assert len(inventory.product_names()) == 6


def test_all_prices_are_positive(inventory):
    assert all(price > 0 for price in inventory.product_prices())


@pytest.mark.parametrize(
    "option, key, reverse",
    [("az", "name", False), ("za", "name", True), ("lohi", "price", False), ("hilo", "price", True)],
)
def test_sorting(inventory, option, key, reverse):
    inventory.sort_by(option)
    values = inventory.product_names() if key == "name" else inventory.product_prices()
    assert values == sorted(values, reverse=reverse)
