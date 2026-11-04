"""Value objects for the checkout domain."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """A catalog item. Prices are integer cents to avoid float rounding."""

    sku: str
    name: str
    price_cents: int


@dataclass(frozen=True)
class CartLine:
    """A sku and how many units of it are in the cart."""

    sku: str
    quantity: int
