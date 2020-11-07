from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict

from src.entity.item import Item
from src.handlers.item import ItemHandler


class Sale:
    """
    Represents a sale-offer entity.
    """

    def __init__(
        self,
        item_uid: str,
        quantity: int,
        price: int,
        seller: str,
        seller_discord_id: int,
        from_date_timestamp: float,
        to_date_timestamp: float,
        sale_uid: str = None,
    ):

        self._item_uid = item_uid
        self._quantity = quantity
        self._price = price
        self._seller = seller
        self._seller_discord_id = seller_discord_id
        self._from_date_timestamp = from_date_timestamp
        self._to_date_timestamp = to_date_timestamp
        self._sale_uid = sale_uid if sale_uid else str(uuid.uuid4())

    @property
    def sale_uid(self) -> str:
        return self._sale_uid

    @property
    def item_uid(self) -> str:
        return self._item_uid

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def price(self) -> int:
        return self._price

    @property
    def seller(self) -> str:
        return self._seller

    @property
    def seller_discord_id(self) -> int:
        return self._seller_discord_id

    @property
    def from_date(self) -> datetime:
        return datetime.fromtimestamp(self._from_date_timestamp)

    @property
    def to_date(self) -> datetime:
        return datetime.fromtimestamp(self._to_date_timestamp)

    @property
    def item(self) -> Item:
        return ItemHandler().uid_search(self._item_uid)  # type: ignore

    @staticmethod
    def from_dict(dic: Dict) -> Sale:
        return Sale(
            item_uid=dic["_item_uid"],
            quantity=dic["_quantity"],
            price=dic["_price"],
            seller=dic["_seller"],
            seller_discord_id=dic["_seller_discord_id"],
            from_date_timestamp=dic["_from_date_timestamp"],
            to_date_timestamp=dic["_to_date_timestamp"],
            sale_uid=dic["_sale_uid"],
        )

    def __str__(self) -> str:
        return "User [{}] offers [{}] units of item [{}] for [{}] coins, from [{}] until [{}]. Sale's UID: {}".format(
            self.seller,
            self.quantity,
            self.item.name,
            self.price,
            self.from_date.date(),
            self.to_date.date(),
            self.sale_uid,
        )
