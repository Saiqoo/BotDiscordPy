import discord
from discord.ext import commands
import discord.ext.commands
import datetime
import json


class Help(commands.Cog):
    """Pour Obtenir la liste des commandes"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="La commande Help", hidden=True)
    async def help(self, ctx, *cog):
        with open("guildconfig.json", "r") as f:
            prefix = json.load(f)
        pre = prefix[str(ctx.guild.id)]["prefix"]

        cogs_name = [c for c in self.bot.cogs]
        cogs_name.remove("Help")
        cogs_name.remove("Setup")
        cogs_name.remove("Log")
        embed = None
        if cog:
            found = False
            for x in cogs_name:
                for y in cog:
                    if x == y:
                        embed = discord.Embed(color=0xCE2029)
                        scog_info = ""
                        for c in self.bot.get_cog(y).get_commands():
                            if not c.hidden:
                                scog_info += f"**{c.name}** - {c.description}\n"
                        embed.set_author(name=f"{cog[0]}", icon_url=f"{self.bot.user.avatar_url}")
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.add_field(name=f"{self.bot.cogs[cog[0]].__doc__}", value=scog_info)
                        embed.add_field(name="Pour obtenir des informations sur la commande :", value=f"Tapez `{pre}help` suivi du nom de la commande", inline=False)
                        found = True
            if not found:
                for x in cogs_name:
                    for c in self.bot.get_cog(x).get_commands():
                        if c.name == cog[0]:
                            if not c.hidden:
                                embed = discord.Embed(color=0xCE2029)
                                embed.set_author(name=f"Commande : {c.name}")
                                embed.timestamp = datetime.datetime.utcnow()
                                embed.add_field(name=f"{c.description}",
                                                value=f"Syntax :\n`{c.qualified_name} {c.signature}`")
        else:
            embed = discord.Embed(color=0xCE2029)
            cogs_desc = ""
            for x in cogs_name:
                cogs_desc += ("**{}** - {}".format(x, self.bot.cogs[x].__doc__) + "\n")
            embed.add_field(name="__Liste des Modules__", value=cogs_desc[0:len(cogs_desc) - 1], inline=False)
            embed.add_field(name="Pour obtenir des informations sur un module :", value=f"Tapez `{pre}help` suivi du nom du module", inline=False)
            embed.set_author(name="Help", icon_url=f"{self.bot.user.avatar_url}")
            embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
