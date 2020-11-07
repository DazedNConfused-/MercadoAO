import hashlib

from unidecode import unidecode

UID_PREFIX: str = "uid:"


class Item:
    """
    Represents a sellable entity.
    """

    def __init__(self, name: str, base_price: int):
        md5 = hashlib.md5()
        md5.update(name.encode(encoding="UTF-8", errors="strict"))
        self._uid = md5.hexdigest()[:8].upper()  # reasonably collision-free UID for dataset
        self._name = name
        self._base_price = base_price

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    @property
    def sanitized_name(self) -> str:
        return unidecode(self._name.lower())

    @property
    def base_price(self) -> int:
        return self._base_price

    def __str__(self) -> str:
        return "{} <{}{}>".format(self.name, UID_PREFIX, self.uid)
