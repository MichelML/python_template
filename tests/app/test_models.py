import dataclasses

import pytest

from app.models import CartLine, Product


def test_product_is_immutable() -> None:
    product = Product(sku="MUG", name="Mug", price_cents=1200)

    with pytest.raises(dataclasses.FrozenInstanceError):
        product.price_cents = 0  # type: ignore[misc]  # asserting the runtime guard


def test_cart_line_is_immutable() -> None:
    line = CartLine(sku="MUG", quantity=2)

    with pytest.raises(dataclasses.FrozenInstanceError):
        line.quantity = 99  # type: ignore[misc]  # asserting the runtime guard


def test_cart_lines_compare_by_value() -> None:
    assert CartLine(sku="MUG", quantity=2) == CartLine(sku="MUG", quantity=2)
