import discord
from discord.ext import commands
import os

bot = commands.Bot(
    command_prefix=["O!", "o!"],
    help_command=None,
    intents = discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(replied_user=False, everyone=False),
    case_insensitive=True
)

token = os.environ["token"]

def restart_bot():
  os.execv(sys.executable, ['python'] + sys.argv)

bot.load_extension("jishaku")

bot.run(token)
