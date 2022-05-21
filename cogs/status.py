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
            resident = emc.Resident("oniyao228", data=await get_data())
            channel = self.bot.get_channel(921312359778230295)
            if resident.online:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f"oniyao228 is online at EarthMC TA", type=3))
                await channel.send("<@798439010594717737> oniyao228 is online at EarthMC TA")
            else:
                await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=f"oniyao228 is offline at EarthMC TA", type=3))
        loop.start()
        

def setup(bot):
    return bot.add_cog(AppCmdVariety(bot))
