from datetime import datetime, timedelta
from typing import Dict, List, Optional

from tinydb import Query, TinyDB

from src.aux.logger import Logger
from src.aux.singleton import Singleton
from src.entity.item import Item
from src.entity.sale import Sale


class SaleHandler(metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()

        self._logger = Logger.get_logger(self.__class__.__name__)
        self._logger.info("Initializing Sale handler...")

        self._db = TinyDB("db/sale.json")

    def create_sale(self, item: Item, quantity: int, price: int, seller: str, seller_id: int) -> Sale:
        result: Sale = Sale(
            item_uid=item.uid,
            quantity=quantity,
            price=price,
            seller=seller,
            seller_discord_id=seller_id,
            from_date_timestamp=datetime.today().timestamp(),
            to_date_timestamp=(datetime.today() + timedelta(days=7)).timestamp(),
        )
        self._db.insert(result.__dict__)

        return result

    def get_sale_by_sale_uid(self, sale_uid: str) -> Optional[Sale]:
        sale = Query()
        result = self._db.get(sale["_sale_uid"] == sale_uid)

        if not result:
            return None
        else:
            return Sale.from_dict(result)

    def get_all_sales(self) -> List[Sale]:
        return self._parse_entities(self._db.all())

    def get_sales_by_item_uid(self, item_uid: str) -> List[Sale]:
        sale = Query()
        return self._parse_entities(self._db.search(sale["_item_uid"] == item_uid))

    def get_sales_by_item_uids(self, item_uids: List[str]) -> List[Sale]:
        sale = Query()
        return self._parse_entities(self._db.search(sale["_item_uid"].one_of(item_uids)))

    def remove_sale_by_sale_uid(self, sale_uid: str) -> int:
        sale = Query()
        return len(self._db.remove(sale["_sale_uid"] == sale_uid))

    def remove_stale_sales(self) -> int:
        sale = Query()
        return len(self._db.remove(sale["_to_date_timestamp"] < datetime.today().timestamp()))

    @staticmethod
    def _parse_entities(entities: List[Dict]) -> List[Sale]:
        return list(map(lambda x: Sale.from_dict(x), entities))
