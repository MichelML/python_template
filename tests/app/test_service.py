import pytest

from app.errors import AppError, InvalidQuantityError, SkuNotInCartError, UnknownSkuError
from app.models import CartLine, Product
from app.service import Cart, Catalog


@pytest.fixture
def catalog() -> Catalog:
    return Catalog(
        [
            Product(sku="TSHIRT", name="T-shirt", price_cents=2000),
            Product(sku="MUG", name="Mug", price_cents=1200),
            Product(sku="STICKER", name="Sticker", price_cents=300),
        ]
    )


@pytest.fixture
def cart(catalog: Catalog) -> Cart:
    return Cart(catalog)


# --- add_item ---------------------------------------------------------------


def test_spec_example_subtotal(cart: Cart) -> None:
    cart.add_item("TSHIRT", 2)
    cart.add_item("MUG", 1)
    cart.add_item("STICKER", 3)

    assert cart.subtotal() == 6100


def test_add_item_creates_a_line(cart: Cart) -> None:
    cart.add_item("MUG", 2)

    assert cart.lines() == [CartLine(sku="MUG", quantity=2)]


def test_add_item_accumulates_quantity_for_same_sku(cart: Cart) -> None:
    cart.add_item("MUG", 2)
    cart.add_item("MUG", 3)

    assert cart.lines() == [CartLine(sku="MUG", quantity=5)]


def test_add_item_rejects_unknown_sku(cart: Cart) -> None:
    with pytest.raises(UnknownSkuError, match="HAT"):
        cart.add_item("HAT", 1)


@pytest.mark.parametrize("quantity", [0, -1, -10])
def test_add_item_rejects_non_positive_quantity(cart: Cart, quantity: int) -> None:
    with pytest.raises(InvalidQuantityError):
        cart.add_item("MUG", quantity)


def test_failed_add_leaves_cart_unchanged(cart: Cart) -> None:
    cart.add_item("MUG", 1)

    with pytest.raises(InvalidQuantityError):
        cart.add_item("MUG", -1)

    assert cart.lines() == [CartLine(sku="MUG", quantity=1)]


# --- remove_item ------------------------------------------------------------


def test_remove_item_decreases_quantity(cart: Cart) -> None:
    cart.add_item("STICKER", 3)
    cart.remove_item("STICKER", 1)

    assert cart.lines() == [CartLine(sku="STICKER", quantity=2)]


def test_remove_item_drops_line_when_quantity_reaches_zero(cart: Cart) -> None:
    cart.add_item("STICKER", 3)
    cart.remove_item("STICKER", 3)

    assert cart.lines() == []


def test_remove_item_more_than_in_cart_drops_line(cart: Cart) -> None:
    cart.add_item("STICKER", 3)
    cart.remove_item("STICKER", 10)

    assert cart.lines() == []


def test_remove_item_leaves_other_lines_untouched(cart: Cart) -> None:
    cart.add_item("MUG", 1)
    cart.add_item("STICKER", 3)
    cart.remove_item("STICKER", 3)

    assert cart.lines() == [CartLine(sku="MUG", quantity=1)]


def test_remove_item_rejects_sku_not_in_cart(cart: Cart) -> None:
    cart.add_item("MUG", 1)

    with pytest.raises(SkuNotInCartError, match="TSHIRT"):
        cart.remove_item("TSHIRT", 1)


def test_remove_item_rejects_sku_already_fully_removed(cart: Cart) -> None:
    cart.add_item("MUG", 1)
    cart.remove_item("MUG", 1)

    with pytest.raises(SkuNotInCartError):
        cart.remove_item("MUG", 1)


def test_remove_item_rejects_unknown_sku(cart: Cart) -> None:
    with pytest.raises(UnknownSkuError, match="HAT"):
        cart.remove_item("HAT", 1)


@pytest.mark.parametrize("quantity", [0, -1, -10])
def test_remove_item_rejects_non_positive_quantity(cart: Cart, quantity: int) -> None:
    cart.add_item("MUG", 1)

    with pytest.raises(InvalidQuantityError):
        cart.remove_item("MUG", quantity)

    assert cart.lines() == [CartLine(sku="MUG", quantity=1)]


# --- subtotal ---------------------------------------------------------------


def test_subtotal_of_empty_cart_is_zero(cart: Cart) -> None:
    assert cart.subtotal() == 0


def test_subtotal_reflects_removals(cart: Cart) -> None:
    cart.add_item("TSHIRT", 2)
    cart.add_item("MUG", 1)
    cart.remove_item("TSHIRT", 1)

    assert cart.subtotal() == 3200


# --- lines ------------------------------------------------------------------


def test_lines_of_empty_cart_is_empty(cart: Cart) -> None:
    assert cart.lines() == []


def test_lines_are_sorted_by_sku(cart: Cart) -> None:
    cart.add_item("TSHIRT", 2)
    cart.add_item("STICKER", 3)
    cart.add_item("MUG", 1)

    assert [line.sku for line in cart.lines()] == ["MUG", "STICKER", "TSHIRT"]


@pytest.mark.parametrize("error", [UnknownSkuError, InvalidQuantityError, SkuNotInCartError])
def test_cart_errors_are_app_errors(error: type[Exception]) -> None:
    assert issubclass(error, AppError)
