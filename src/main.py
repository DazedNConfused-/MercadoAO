from discord.ext.commands import Context

from src.aux.configuration import Configuration
from src.bot import MercadoAO
from src.command_handler import CommandHandler

# read parameters from configuration -----------------------------------------------------------------------------------

configuration = Configuration()
if not configuration.get_discord_token():
    raise Exception("No Discord token defined in config.ini")

# initialize bot -------------------------------------------------------------------------------------------------------

version = "0.1 Alpha"
bot = MercadoAO(
    command_prefix="$",
    case_insensitive=True,
    description="MercadoAO Bot - Version {}".format(version),
)
commandHandler = CommandHandler()

# define bot commands --------------------------------------------------------------------------------------------------


@bot.command(name="buy")
async def buy(ctx, sale_uid: str = None):
    """
    Claims an ongoing sale as a buyer, effectively ending it and notifying all parties with details of the transaction.

    :param sale_uid: The Sale's UID.
    """

    if not sale_uid:
        await ctx.author.send("The Sale's UID is required in order to buy!")
        return

    await commandHandler.buy_handler(ctx=ctx, sale_uid=sale_uid)


@bot.command(name="sell")
async def sell(ctx, item_to_sell: str = None, quantity: int = None, price: int = None):
    """
    Publishes a sale. It will be listed on the market for a whole week.

    :param item_to_sell: The item to be sold. Accepts both item names or a specific UID.
    :param quantity: The quantity of items to be sold.
    :param price: The final price for the whole batch of units.
    """

    if not item_to_sell or not quantity or not price:
        await ctx.author.send(
            "All params ([item_to_sell] [quantity] [price]) must be specified in order to make a sale!"
        )
        return

    await commandHandler.sell_handler(
        ctx=ctx,
        item_to_sell=item_to_sell,
        quantity=quantity,
        price=price,
        announce=configuration.get_announcement_channel_id() is not None,
        announcement_channel_id=configuration.get_announcement_channel_id(),
    )


@bot.command(name="list")
async def sale_list(ctx: Context, query: str = None):
    """
    Returns a list of all undergoing sales for the given search query.

    Accepts both item names or a specific UID (which can be searched by either passing the UID directly or prefixing it
    with 'uid:')

    If query is unspecified, returns all current offerings.

    :param query: The string to be searched.
    """

    if not query:
        await commandHandler.list_all_handler(ctx)
    else:
        await commandHandler.list_handler(ctx, query)


@bot.command(name="search")
async def search(ctx: Context, query: str = None):
    """
    Returns the list of valid items that may be exchanged using the bot for the given search query.

    Accepts both item names or a specific UID (which can be searched by either passing the UID directly or prefixing it
    with 'uid:')

    For example: '"Daga de Plata"', 'uid:E3622EA7' or 'E3622EA7' are all valid search queries for the same item.

    :param query: The string to be searched.
    """

    if not query:
        await ctx.author.send("You must specify something to search!")
        return

    await commandHandler.search_handler(ctx, query)


@bot.command(name="uid")
async def search_uid(ctx: Context, query: str = None):
    """
    Searches for the item that corresponds to the given UID.

    :param query: The UID to be searched.
    """
    if not query:
        await ctx.author.send("You must specify something to search!")
        return

    await commandHandler.search_uid_handler(ctx, query)


# execute bot main loop / start listening to server --------------------------------------------------------------------

bot.run(configuration.get_discord_token())
