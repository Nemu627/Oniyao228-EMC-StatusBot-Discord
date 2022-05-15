import discord
from discord.ext import commands, tasks
import os
from typing import Tuple

bot = commands.Bot(
    command_prefix=["O!", "o!"],
    help_command=None,
    intents = discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(replied_user=False, everyone=False),
    case_insensitive=True
)

token = os.environ["token"]

bot.load_extension("jishaku")

def get_data() -> Tuple[dict, dict]:
    resp_town = get("https://earthmc.net/map/aurora/tiles/_markers_/marker_earth.json")
    resp_town.raise_for_status()
    resp_player = get("https://earthmc.net/map/aurora/up/world/earth/")
    resp_player.raise_for_status()
    town_data = resp_town.json()["sets"]["townyPlugin.markerset"]["areas"]
    towns = {name[:-3].lower(): town[1] for name, town in zip(town_data, town_data.items()) if name.endswith("__0")}
    for town in towns:
        towns[town]["desc"] = [desc for desc in split(r"<[^<>]*>", towns[town]["desc"]) if desc != ""]
    return towns, resp_player.json()

def search_online(name: "oniyao228", *, data: Tuple[dict, dict] = None):
    data = get_data()
    res_data = next((person for person in data[1]["players"] if person["account"] == name), None)
    if res_data is not None:
        online = True
    else:
        online = False
    return online
    

@tasks.loop(seconds=10)
async def loop():
    oniya = search_online()
    if oniya.online:
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f"Oniyao228 is online at EarthMC TA", type=3))
    else:
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=f"Oniyao228 is offline at EarthMC TA", type=3))
            
loop.start()

bot.run(token)
