from __future__ import annotations

import asyncio
from asyncio import Task

from src.aux.logger import Logger
from src.aux.singleton import Singleton
from src.handler.sale import SaleHandler


class StaleOfferCleanupJob(metaclass=Singleton):

    _task: Task

    def __init__(self) -> None:
        super().__init__()

        self._logger = Logger(self.__class__.__name__)
        self._logger.info("Initializing stale offers cleanup job...")
        self._sale_handler = SaleHandler()

    async def _run(self) -> None:
        self._logger.info("Stale offers scheduler started successfully. Will run once per hour.")
        while True:
            # execute task
            self._logger.info("Executing stale offers cleanup task...")

            removed_entries: int = self._sale_handler.remove_stale_sales()

            self._logger.info("Removed {} stale entries.".format(removed_entries))

            # wait before next iteration
            await asyncio.sleep(3600)

    def start(self) -> StaleOfferCleanupJob:
        self._task = asyncio.get_event_loop().create_task(self._run())
        return self

    def stop(self) -> bool:
        return self._task.cancel()
