from discord.ext import commands
import sys


def setup(bot):
    bot.add_cog(Inutile(bot))


class Inutile(commands.Cog):
    """Liste de commandes Inutiles"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description="Obtenir le pseudo de l'owner "
    )
    async def owner(self, ctx):
        await ctx.channel.send(str(ctx.guild.owner))

    @commands.command(
        description="Voir le salon actuel"
    )
    async def salon(self, ctx, channel):
        await ctx.send(f"Le salon est {channel}")

    @commands.command()
    async def createur(self, ctx):
        await ctx.send("J'ai été crée par **Saiqo**")

    @commands.command(
        description="Afficher la version du système"
    )
    async def sys_version(self, ctx):
        await ctx.send(sys.version)

