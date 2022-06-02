import discord
from discord.ext import commands
import discord.ext.commands
import datetime
import json


def setup(bot):
    bot.add_cog(Setup(bot))


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlogs(self, ctx, channel: discord.TextChannel = None):
        channel_id = channel.id
        if channel is not None:
            with open("guildconfig.json", "r") as f:
                chan = json.load(f)

            chan[str(ctx.guild.id)]["logs"] = channel_id

            with open("guildconfig.json", "w") as f:
                json.dump(chan, f, sort_keys=True, indent=4, ensure_ascii=False)

            await ctx.channel.send(f"Le salon de logs est désormais : <#{channel.id}>")
        else:
            await ctx.channel.send("Vous n'avez pas donné de nom de salon")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel = None):
        channel_id = channel.id
        if channel is not None:
            with open("guildconfig.json", "r") as f:
                chan = json.load(f)

            chan[str(ctx.guild.id)]["welcome"] = channel_id
            with open("guildconfig.json", "w") as f:
                json.dump(chan, f, sort_keys=True, indent=4, ensure_ascii=False)

            await ctx.channel.send(f"Le salon d'acceuil des membres est désormais <#{channel.id}>")

        else:
            await ctx.channel.send("Vous n'avez pas spécifié de nom de salon")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setgoodbye(self, ctx, channel: discord.TextChannel = None):
        channel_id = channel.id
        if channel is not None:
            with open("guildconfig.json", "r") as f:
                chan = json.load(f)

            chan[str(ctx.guild.id)]["goodbye"] = channel_id
            with open("guildconfig.json", "w") as f:
                json.dump(chan, f, sort_keys=True, indent=4, ensure_ascii=False)

            await ctx.channel.send(f"Le salon de départ des membres est désormais <#{channel.id}>")

        else:
            await ctx.channel.send("Vous n'avez pas spécifié de nom de salon")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
        if len(prefix) > 5:
            await ctx.send("Le nouveau préfix de ne peut pas dépasser les 5 caractères")
        else:
            with open("guildconfig.json", "r") as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)]["prefix"] = prefix

            with open("guildconfig.json", "w") as f:
                json.dump(prefixes, f, indent=4)

            await ctx.send(f"Le nouveau prefix est désormais `{prefix}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, commande):
        com = self.bot.get_command(commande)
        if com in self.bot.commands:
            with open("commandes.json", "r") as f:
                cmd = json.load(f)
            com2 = cmd[str(ctx.guild.id)]
            if commande not in com2:
                with open("commandes.json", "w") as f:
                    cmd[str(ctx.guild.id)][str(commande)] = False
                    json.dump(cmd, f, sort_keys=True, indent=4, ensure_ascii=False)
                await ctx.send(f"La commande `{commande}` a été désactivé !")
            else:
                await ctx.send(f"La commande `{commande}` est déja désactivé")
        else:
            await ctx.send("La commande que vous voulez désactiver n'existe pas !")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, commande):
        with open("commandes.json", "r") as f:
            cmd = json.load(f)
        com = cmd[str(ctx.guild.id)]
        if commande in com:
            del cmd[str(ctx.guild.id)][str(commande)]

            with open("commandes.json", "w") as f:
                json.dump(cmd, f, sort_keys=True, indent=4, ensure_ascii=False)
            await ctx.send(f"La commande `{commande}` a été activé !")
        else:
            await ctx.send("La commande que vous voulez activer n'existe pas / est déja activé")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable_fonct(self, ctx, channel: str):
        if channel == "welcome" or channel == "goodbye" or channel == "logs":
            with open("guildconfig.json", "r") as f:
                salon = json.load(f)
            salon[str(ctx.guild.id)][f"{channel}"] = 0
            with open("guildconfig.json", "w") as f:
                json.dump(salon, f, sort_keys=True, indent=4, ensure_ascii=False)

            if channel == "welcome":
                await ctx.send("Le message d'acceuil des membres est désactivé")
            if channel == "goodbye":
                await ctx.send("Le message de départ des membres est désactivé")
            if channel == "logs":
                await ctx.send("Les logs sont maintenant désactivées !")
        else:
            await ctx.send("Vous ne pouvez pas désactivé ce salon")
