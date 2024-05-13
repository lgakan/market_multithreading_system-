from dataclasses import dataclass, field

from .seller import Seller


@dataclass(order=True)
class SellerQuantity:
    quantity: int
    seller: Seller = field(compare=False)
    is_busy: bool = field(compare=False, default=False)
