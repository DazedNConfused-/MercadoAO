import textwrap
import time
from typing import List, Optional, Set

from discord import User
from discord.ext.commands import Context

from src.aux.logger import Logger
from src.entity.item import Item
from src.entity.sale import Sale
from src.handlers.item import ItemHandler
from src.handlers.sale import SaleHandler


class CommandHandler:
    def __init__(self) -> None:
        super().__init__()
        self._logger = Logger.get_logger(self.__class__.__name__)

        self._logger.info("Initializing command handler...")
        self._item_handler = ItemHandler()
        self._sale_handler = SaleHandler()

    async def sell_handler(
        self,
        ctx: Context,
        item_to_sell: str,
        quantity: int,
        price: int,
        announce: bool,
        announcement_channel_id: Optional[int],
    ):
        self._logger.debug(
            "[SELL] - [{}] command called by [{}] with arguments [{}] [{}] [{}]".format(
                ctx.command, ctx.author, item_to_sell, quantity, price
            )
        )

        item: Item
        if self._item_handler.is_uid(query=item_to_sell):
            item = self._item_handler.uid_search(uid=item_to_sell)  # type: ignore
        else:
            search: Set[Item] = self._item_handler.search(search_param=item_to_sell)
            if len(search) != 1:
                await self.send_partitioned_message(
                    ctx.author,
                    "Your sale of [{}] matched multiple items. "
                    "Please make your offer again with a more specific argument (uid's are also accepted). "
                    "Potential matches: {}".format(item_to_sell, set(map(lambda x: str(x), search))),
                )
                return
            item = search.pop()

        sale: Sale = self._sale_handler.create_sale(
            item=item, quantity=quantity, price=price, seller=str(ctx.author), seller_id=ctx.author.id
        )

        await ctx.author.send(
            "Your sale of [{}] units of [{}] for [{}] has been accepted and published".format(
                sale.quantity, item.name, sale.price
            )
        )

        if announce and announcement_channel_id:
            await self.send_announcement(ctx, announcement_channel_id, str(sale))

    async def buy_handler(self, ctx: Context, sale_uid: str):
        self._logger.debug(
            "[BUY] - [{}] command called by [{}] with argument [{}]".format(ctx.command, ctx.author, sale_uid)
        )

        sale: Optional[Sale] = self._sale_handler.get_sale_by_sale_uid(sale_uid=sale_uid)

        if not sale:
            await ctx.author.send(
                "Your buy request for ID [{}] did not match any ongoing sales. Maybe it has been bought already? "
                "Check ID and try again.".format(sale_uid)
            )
            return

        buyer: User = ctx.author
        await ctx.author.send(
            "Congratulations! You have bought [{}] units of [{}] for [{}]! "
            "I have already DMed the seller [{}] with details of the transaction. "
            "Message him to complete delivery.".format(sale.quantity, sale.item, sale.price, sale.seller)
        )
        await self.get_user_by_id(ctx, user_id=sale.seller_discord_id).send(
            "Congratulations! Your sale of [{}] units of [{}] for [{}] has been bought by [{}]! "
            "DM buyer to complete the transaction!".format(sale.quantity, sale.item, sale.price, buyer)
        )
        self._sale_handler.remove_sale_by_sale_uid(sale.sale_uid)

    async def list_all_handler(self, ctx: Context):
        self._logger.debug("[LIST ALL] - [{}] command called by [{}]".format(ctx.command, ctx.author))

        search_results: List[Sale] = self._sale_handler.get_all_sales()

        if not search_results:
            await ctx.author.send("No sales currently going on")
        else:
            await ctx.author.send("The following sales are currently undergoing:")
            await self.send_partitioned_message(ctx.author, "\n".join(str(sale) for sale in search_results))

    async def list_handler(self, ctx: Context, query: str):
        self._logger.debug(
            "[LIST] - [{}] command called by [{}] with argument [{}]".format(ctx.command, ctx.author, query)
        )

        search_results: List[Sale]
        sanitized_uid: Optional[str] = self._item_handler.sanitize_uid(uid=query)
        if sanitized_uid:
            search_results = self._sale_handler.get_sales_by_item_uid(item_uid=sanitized_uid)
        else:
            search_results = self._sale_handler.get_sales_by_item_uids(
                list(map(lambda x: x.uid, self._item_handler.search(search_param=query)))
            )

        if not search_results:
            await ctx.author.send("No sales currently going on for query [{}]".format(query))
        else:
            await ctx.author.send("The following sales are currently undergoing for query [{}]:".format(query))
            await self.send_partitioned_message(ctx.author, "\n".join(str(sale) for sale in search_results))

    async def search_handler(self, ctx: Context, query: str):
        self._logger.debug(
            "[SEARCH] - [{}] command called by [{}] with argument [{}]".format(ctx.command, ctx.author, query)
        )

        if self._item_handler.is_uid(query=query):  # if UID is detected, redirect to UID handler
            self._logger.debug("UID detected. Redirecting to UID search handler...")
            await self.search_uid_handler(ctx, query)
            return

        start = time.time()
        search_results: Set[Item] = self._item_handler.search(search_param=query)
        end = time.time()

        if not search_results:
            await ctx.author.send("Your search for ['{}'] awarded 0 results.".format(query))
        else:
            await self.send_partitioned_message(
                ctx.author,
                "Your search for ['{}'] awarded {} and was completed in {} seconds.".format(
                    query, set(map(lambda x: str(x), search_results)), round(end - start, 4)
                ),
            )

    async def search_uid_handler(self, ctx: Context, item_uid: str):
        self._logger.debug(
            "[UID SEARCH] - [{}] command called by [{}] with argument [{}]".format(ctx.command, ctx.author, item_uid)
        )

        start = time.time()
        search_result: Optional[Item] = self._item_handler.uid_search(uid=item_uid)
        end = time.time()

        if not search_result:
            await ctx.author.send("Your search for ['{}'] awarded 0 results.".format(item_uid))
        else:
            await self.send_partitioned_message(
                ctx.author,
                "Your search for ['{}'] awarded [{}] and was completed in {} seconds.".format(
                    item_uid, str(search_result), round(end - start, 4)
                ),
            )

    async def send_announcement(self, ctx: Context, channel_id: int, msg: str):
        """
        Sends a global announcement to the given channel

        :param ctx: The message's Context.
        :param channel_id: The target Channel's ID.
        :param msg: The message to send.
        """
        channel = ctx.bot.get_channel(channel_id)
        if channel is not None:
            self._logger.info("Announcing message [{}] in channel [{}]".format(msg, str(channel)))
            await channel.send(msg)
        else:
            self._logger.error(
                "Should have announced message in channel [{}], but it couldn't be found".format(str(channel))
            )

    @staticmethod
    def get_user_by_id(ctx: Context, user_id: int) -> User:
        """
        Retrieves the corresponding Discord's User by ID.

        :param ctx: The search's Context.
        :param user_id: The ID to be searched.
        """
        return ctx.bot.get_user(user_id)

    @staticmethod
    async def send_partitioned_message(target: Context, msg: str, wrap_at=2000):
        """
        Sends a message to Author/Channel, honoring Discord's maximum message length.

        :param target: The message's Context.
        :param msg: The message to partition.
        :param wrap_at: The maximum message length. Defaults to Discord's max.
        """
        for line in textwrap.wrap(text=msg, width=wrap_at, replace_whitespace=False):
            await target.send(line)
