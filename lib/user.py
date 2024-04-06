from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Union, Generator, Tuple, Dict

from lib.item import Item, ItemType


class AbstractUser(ABC):
    def __init__(self, user_id: int):
        self.user_id = user_id

    @staticmethod
    def gen_list(obj) -> Generator[Tuple[str, List[Item]], None, None]:
        for atr_name, atr in obj.__dict__.items():
            #print(atr_name, atr)
            if isinstance(atr, list):
                yield atr_name, atr

    @staticmethod
    def str(obj) -> Dict[str, str]:
        output_str_dict = {
            atr_name: "\n".join([f"{idx}. {str(item)}" for idx, item in enumerate(atr, start=1)])
            for atr_name, atr in obj.gen_list(obj)
        }
        return output_str_dict

    @staticmethod
    def find_item_by_item_type(item_type: ItemType, lst: List[Item]) -> Union[Item, None]:
        for item in lst:
            if item.item_type == item_type:
                return item

        return None
