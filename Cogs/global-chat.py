import discord
from discord.ext import commands

class AppCmdGlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return
        topic = "oniyama-gc-test"
        if message.channel.topic == topic:
            for c in self.bot.get_all_channels():
                if c.category is None:
                    continue
                for channel in c.category.text_channels:
                    if channel.topic == topic:
                        if channel == message.channel:
                            continue
                        embed=discord.Embed(description=message.content, color=0x9B95C9)
                        embed.set_author(name=f"{message.author}",icon_url=message.author.avatar.url)
                        embed.set_footer(text=f"{message.guild.name}",icon_url=message.guild.icon.url)
                        if message.attachments != []:
                            embed.set_image(url=message.attachments[0].url)
                        if message.reference:
                            reference_msg = await message.channel.fetch_message(message.reference.message_id)
                            if reference_msg.embeds and reference_msg.author == self.bot.user:
                                reference_message_content = reference_msg.embeds[0].description
                                reference_message_author = reference_msg.embeds[0].author.name
                            elif reference_msg.author != self.bot.user:
                                reference_message_content = reference_msg.content
                                reference_message_author = reference_msg.author.name+'#'+reference_msg.author.discriminator
                            reference_content = ""
                            for string in reference_message_content.splitlines():
                                reference_content += "> " + string + "\n"
                            embed.add_field(name=reference_message_author.name, value=reference_content, inline=True)
                        await channel.send(embed=embed)
    
def setup(bot):
    return bot.add_cog(AppCmdGlobalChat(bot))
