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
            resident = emc.Resident("oniya0228", data=await get_data())
            if resident.online:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f"Oniyao228 is online at EarthMC", type=3))
            else:
                await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=f"Oniyao228 is offline at EarthMC", type=3))
        loop.start()
        
    @commands.command(aliases=["t"])
    async def town(self, ctx, town_to_find="Oniyama"):
        try:
            async with ctx.typing():
                town = emc.Town(town_to_find, data=await get_data())
        except emc.exceptions.TownNotFoundException:
            embed = discord.Embed(title=f"The town {town_to_find} was not found", colour=0xb00e0e)
        else:
            embed = discord.Embed(title=town.name, colour=int(town.colour[1:], 16))
            embed.add_field(name="Mayor", value=f"```{town.mayor}```")
            embed.add_field(name="nation", value=f"```{town.nation}```")
            embed.add_field(name="Flags", value=f"""```diff
{'+' if town.flags['capital'] else '-'} Capital
{'+' if town.flags['fire'] else '-'} Fire
{'+' if town.flags['explosions'] else '-'} Explosions
{'+' if town.flags['mobs'] else '-'} Mobs
{'+' if town.flags['pvp'] else '-'} PVP
```""")
            _long_fields(embed, f"Residents [{len(town.residents)}]", [res.name for res in town.residents])
            online = [res.name for res in town.residents if res.online]
            if len(online) > 0:
                embed.add_field(name=f"Online residents [{len(online)}]", value=f"```{', '.join(online)}```", inline=False)
            else:
                embed.add_field(name="Online residents [0]", value=f"```No online residents in {town}```", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["n"])
    async def nation(self, ctx, nation_to_find="Grasberg"):
        try:
            async with ctx.typing():
                nation = emc.Nation(nation_to_find, data=await get_data())
        except emc.exceptions.NationNotFoundException:
            embed = discord.Embed(title=f"The nation {nation_to_find} was not found", colour=0xb00e0e)
        else:
            embed = discord.Embed(title=nation.name, colour=int(nation.colour[1:], 16))
            embed.add_field(name="Leader", value=f"```{nation.leader}```")
            embed.add_field(name="Capital", value=f"```{nation.capital}```")
            embed.add_field(name="Population", value=f"```{len(nation.citizens)}```")
            _long_fields(embed, f"Towns [{len(nation.towns)}]", [town.name for town in nation.towns])
            online = [res.name for res in nation.citizens if res.online]
            if len(online) > 0:
                embed.add_field(name=f"Online [{len(online)}]", value=f"```{', '.join(online)}```", inline=False)
            else:
                embed.add_field(name="Online [0]", value=f"```0 citizens online in {nation}```", inline=False)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=["res", "player", "pl"])
    async def resident(self, ctx, resident_to_find="oniyao228"):
        async with ctx.typing():
            resident = emc.Resident(resident_to_find, data=await get_data())
        embed = discord.Embed(title=resident.name, colour=0x0a8cf0)
        embed.set_thumbnail(url=f"https://minotar.net/armor/bust/{resident}")
        embed.add_field(name="Town", value=f"```{resident.town}```")
        embed.add_field(name="Nation", value=f"```{resident.nation}```")
        if resident.online:
            if resident.hidden:
                embed.add_field(name="Position", value=f"```{resident} is currently not visable on the map```")
            else:
                embed.add_field(name="Position", value=f"```{resident.position[0]}/{resident.position[1]}/{resident.position[2]}```([map]({emc.util.map_link(resident.position)}))")
        else:
            embed.add_field(name="Position", value=f"```{resident} is currently offline```")
        await ctx.send(embed=embed)

def setup(bot):
    return bot.add_cog(AppCmdVariety(bot))
