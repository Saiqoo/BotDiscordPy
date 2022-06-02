from datetime import datetime
import discord
from discord.ext.commands import Cog
import json


def setup(bot):
    bot.add_cog(Log(bot))


class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_delete(self, message):
        with open("guildconfig.json", "r") as f:
            chan = json.load(f)
        logchannel = chan[str(message.guild.id)]["logs"]
        log_channel = self.bot.get_channel(logchannel)
        if not logchannel == 0:
            if not message.author.bot:
                embed = discord.Embed(colour=0xCE2029,
                                      timestamp=datetime.utcnow(),
                                      description=f"**Message envoyé par {message.author.mention} supprimé dans {message.channel.mention} **\n{message.content}")
                embed.set_author(name="Message supprimé", icon_url=f"{message.author.avatar_url}")
                await log_channel.send(embed=embed)
        else:
            pass
