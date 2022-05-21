import discord
from discord.ext import commands


token = os.environ["token"]

bot = commands.Bot(
    command_prefix=["O!", "o!"],
    help_command=None,
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(replied_user=False, everyone=False),
    case_insensitive=True
)

bot.load_extension("jishaku")

bot.load_extension("cogs.status")

bot.run(token)
