"""Checkout use cases: catalog lookup and the cart."""

from collections.abc import Iterable

from app.errors import InvalidQuantityError, SkuNotInCartError, UnknownSkuError
from app.models import CartLine, Product


class Catalog:
    """Products indexed by sku for O(1) lookup."""

    def __init__(self, products: Iterable[Product]) -> None:
        self._products = {product.sku: product for product in products}

    def get(self, sku: str) -> Product:
        product = self._products.get(sku)
        if product is None:
            raise UnknownSkuError(sku)
        return product


class Cart:
    """A shopper's cart: quantities per sku, priced against a catalog."""

    def __init__(self, catalog: Catalog) -> None:
        self._catalog = catalog
        self._quantities: dict[str, int] = {}

    def add_item(self, sku: str, quantity: int) -> None:
        self._validate(sku, quantity)
        self._quantities[sku] = self._quantities.get(sku, 0) + quantity

    def remove_item(self, sku: str, quantity: int) -> None:
        """Remove up to `quantity` units; the line disappears once it reaches zero."""
        self._validate(sku, quantity)
        current = self._quantities.get(sku)
        if current is None:
            raise SkuNotInCartError(sku)
        remaining = current - quantity
        if remaining > 0:
            self._quantities[sku] = remaining
        else:
            del self._quantities[sku]

    def subtotal(self) -> int:
        return sum(
            self._catalog.get(sku).price_cents * quantity
            for sku, quantity in self._quantities.items()
        )

    def lines(self) -> list[CartLine]:
        return [
            CartLine(sku=sku, quantity=quantity)
            for sku, quantity in sorted(self._quantities.items())
        ]

    def _validate(self, sku: str, quantity: int) -> None:
        # Validate everything before mutating, so a failed call leaves the cart unchanged.
        if quantity <= 0:
            raise InvalidQuantityError(quantity)
        self._catalog.get(sku)
