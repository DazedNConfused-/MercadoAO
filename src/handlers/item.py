import difflib
import json
from typing import Iterable, List, Optional, Set

import unidecode

from src.aux.logger import Logger
from src.aux.singleton import Singleton
from src.entity.item import UID_PREFIX, Item


class ItemHandler(metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()

        self._logger = Logger.get_logger(self.__class__.__name__)
        self._logger.info("Initializing Item handler...")

        self._logger.info("Loading item list...")
        self._items: Set[Item] = set()

        with open("resources/items.json") as json_file:
            data = json.load(json_file)

            for i in data:
                if i["precio"] != "-":
                    item2add: Item = Item(i["nombre"], i["precio"])

                    if any(item2add.uid == item.uid for item in self._items):
                        # this scenario is _EXTREMELY_ unlikely is dataset was correct to begin with.
                        # collision(s) are a strong indicator of repeated items inside dataset.
                        raise Exception(
                            "Item UID collision detected with item {}. Aborting operation.".format(item2add)
                        )

                    self._items.add(item2add)

        self._logger.info("Loaded {} sellable items...".format(self._items.__len__()))

    def is_uid(self, query: str) -> bool:
        """
        Returns whether the given query should be considered an UID or not.

        :param query: The string to search.
        :return:
        """
        return UID_PREFIX in query or self.uid_search(query) is not None

    def sanitize_uid(self, uid: str) -> Optional[str]:
        """
        Returns a sanitized UID (a UID without prefix, if applicable); or None if given parameter was not an UID.

        :param uid: The UID to sanitize.
        """
        return uid.replace(UID_PREFIX, "") if self.is_uid(uid) else None

    def uid_search(self, uid: str) -> Optional[Item]:
        """
        Returns the Item that matches the given UID, or None if there was no match.

        :param uid: the UID to search for.
        :return:
        """
        uid = uid.replace(UID_PREFIX, "")
        return next((item for item in self._items if item.uid.__eq__(uid)), None)

    def search(self, search_param: str) -> Set[Item]:
        """
        Returns a list of potentially sellable Item(s) from the game that match the given query.

        It uses a mix between literal substring comparisons and difflib's SequenceMatcher. The best matches among the
        possibilities are returned in a set.

        :param search_param: word for which close matches are desired
        :return: a list of the best "good enough" matches.
        """

        # initialize search ---

        search_param = unidecode.unidecode(search_param.lower())  # sanitize input

        def sequence_matcher(items: Iterable[Item], n: int, cutoff: float) -> List[Item]:  # define aux fuzzy matcher
            matches: List = list()
            for item in items:
                if len(matches) > n:
                    break
                if difflib.SequenceMatcher(None, search_param, item.sanitized_name).ratio() >= cutoff:
                    matches.append(item)
            return matches

        # execute search algorithm ---

        full_match: Item = next((item for item in self._items if item.sanitized_name.__eq__(search_param)), None)  # type: ignore
        if full_match is not None:
            return {full_match}  # if we got one full match, stop searching - save resources

        # if we didn't get one full match, we are going to do a best-effort fuzzy search
        substring_name_matches: Set[Item] = set(
            filter(lambda x: True if search_param in x.sanitized_name else False, self._items)
        )
        fuzzy_name_matches: List[Item] = sequence_matcher(self._items, 100, 0.6)

        substring_name_matches.update(fuzzy_name_matches)

        return substring_name_matches
