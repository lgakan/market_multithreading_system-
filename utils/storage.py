from dataclasses import dataclass, field
from typing import Union, Dict, List, Any

from utils.item import Item, ItemType


@dataclass
class Storage:
    inventory: Dict[ItemType, Item] = field(default_factory=dict)

    @classmethod
    def inventory_from_list(cls, inventory_list: List[Item]):
        init_inventory = []
        for item in inventory_list:
            if item.item_type != item.item_type:
                raise Exception(f"{item.item_type} doesn't match {item}")
            if item.quantity > 0:
                init_inventory.append(item)
        return cls({item.item_type: item for item in inventory_list})

    def find_item_by_item_type(self, item_type: ItemType) -> Union[Item, None]:
        return self.inventory.get(item_type)

    def __str__(self) -> str:
        return f"Inventory: {self.inventory}"
