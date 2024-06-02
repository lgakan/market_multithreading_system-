from dataclasses import dataclass, field

from .seller import Seller


@dataclass(order=True)
class SellerPriority:
    priority: int
    seller: Seller = field(compare=False)
