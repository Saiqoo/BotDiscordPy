from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command
import json


class Info(Cog):
    """Liste des commandes d'informations"""
    def __init__(self, bot):
        self.bot = bot

    @command(name="userinfo", aliases=["memberinfo", "ui", "mi"], description="Informations sur un utilisateur")
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        embed = Embed(title=f"Informations sur {target}",
                      colour=target.colour,
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=target.avatar_url)

        fields = [("Pseudo", str(target), True),
                  ("ID", target.id, True),
                  ("Bot ?", target.bot, True),
                  ("Grade le plus haut ", target.top_role.mention, True),
                  ("Statut", str(target.status).title(), True),
                  ("Activité",
                   f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}",
                   True),
                  ("Compte crée le", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("A rejoint le serveur le", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Boosté ?", bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name="servinfo", aliases=["guildinfo", "si", "gi"], description="Informations sur le serveur")
    async def server_info(self, ctx):
        embed = Embed(title="Information du Serveur",
                      color=0xCE2029,
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("ID", ctx.guild.id, True),
                  ("Owner", ctx.guild.owner, True),
                  ("Région", ctx.guild.region, True),
                  ("Date création", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Membre", len(ctx.guild.members), True),
                  ("Utilisateurs", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Membre banni", len(await ctx.guild.bans()), True),
                  ("Statut", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                  ("Channels Textuels", len(ctx.guild.text_channels), True),
                  ("Channels Vocaux", len(ctx.guild.voice_channels), True),
                  ("Catégories", len(ctx.guild.categories), True),
                  ("Rôles", len(ctx.guild.roles), True),
                  ("Invites", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(description="Obtenir la liste des commandes désactivé")
    async def com_disable(self, ctx):
        with open("commandes.json", "r") as f:
            disable = json.load(f)
            liste = disable[str(ctx.guild.id)]
        result = ""
        for cle in liste.keys():
            result += f"- {cle}\n"
        if liste:
            embed = Embed(title="Commandes désactivés sur le serveur :",
                          description=f"{result}",
                          color=0xCE2029,
                          timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            await ctx.send("Aucune commande n'est désactivé sur ce serveur")


def setup(bot):
    bot.add_cog(Info(bot))
