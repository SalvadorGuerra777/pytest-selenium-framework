BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


def test_cart_starts_empty(inventory):
    assert inventory.cart_count() == 0


def test_add_items_updates_badge_and_cart(inventory):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    assert inventory.cart_count() == 2
    assert inventory.open_cart().item_names() == [BACKPACK, BIKE_LIGHT]


def test_remove_item_from_inventory_page(inventory):
    inventory.add_to_cart(BACKPACK)
    inventory.remove_from_cart(BACKPACK)
    assert inventory.cart_count() == 0
    assert inventory.open_cart().item_names() == []
