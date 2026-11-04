"""Exception hierarchy for the application."""


class AppError(Exception):
    """Base class for all expected, domain-level errors raised by the app."""


class UnknownSkuError(AppError):
    """Raised when a sku is not in the catalog."""

    def __init__(self, sku: str) -> None:
        super().__init__(f"Unknown sku: {sku!r}")
        self.sku = sku


class InvalidQuantityError(AppError):
    """Raised when a quantity is not a positive integer."""

    def __init__(self, quantity: int) -> None:
        super().__init__(f"Quantity must be positive, got {quantity}")
        self.quantity = quantity


class SkuNotInCartError(AppError):
    """Raised when removing a sku that has no line in the cart."""

    def __init__(self, sku: str) -> None:
        super().__init__(f"Sku not in cart: {sku!r}")
        self.sku = sku
