import discord
from discord.ext import commands, tasks
import emc
from emc.async_ import get_data

class AppCmdVariety(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        @tasks.loop(seconds=10)
        async def loop():
            resident = emc.Resident("Oniya0228", data=await get_data())
            if resident.online:
                await self.bot.change_presence(status=discord.Status.online,
                                               activity=discord.Activity(name=f"Oniyao228 is online at EarthMC",
                                                                         type=3))
            else:
                await self.bot.change_presence(status=discord.Status.idle,
                                               activity=discord.Activity(name=f"Oniyao228 is offline at EarthMC",
                                                                         type=3))
        loop.start()

def setup(bot):
    return bot.add_cog(AppCmdVariety(bot))
