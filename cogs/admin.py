import discord
from discord.ext import commands
import datetime
import asyncio
import json


def setup(bot):
    bot.add_cog(Moderation(bot))


async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name="Muted",
                                            permissions=discord.Permissions(
                                                send_messages=False,
                                                speak=False),
                                            reason="Creaion du role Muted pour mute les personnes pas sage")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages=False, speak=False)
    return mutedRole


async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    return await createMutedRole(ctx)


class Moderation(commands.Cog):
    """Liste des commandes de modération"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description="Permet de kick un utilisateur"
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"**{member} a été kick** \n**Raison** : {reason}")

        with open("guildconfig.json", "r") as f:
            chan = json.load(f)
        logchannel = chan[str(ctx.guild.id)]["logs"]
        log_channel = self.bot.get_channel(logchannel)

        embed = discord.Embed(
            color=0xCE2029, description=f"**{ctx.author.mention}** a kick **{member}** \n**Raison : **{reason}"
        )
        embed.set_author(name="Membre Kick", icon_url=f"{member.avatar_url}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"ID : {member.id}", icon_url=f"{self.bot.user.avatar_url}")
        await log_channel.send(embed=embed)

    @commands.command(
        description="Permet de Bannir un utilisateur"
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        await ctx.guild.ban(member, reason=reason)

        await ctx.send(f"**{member} a été banni** \n**Raison** : {reason}")
        with open("guildconfig.json", "r") as f:
            chan = json.load(f)
        logchannel = chan[str(ctx.guild.id)]["logs"]
        log_channel = self.bot.get_channel(logchannel)

        embed = discord.Embed(
            color=0xCE2029, description=f"**{ctx.author.mention}** a banni **{member}** \n**Raison : **{reason}"
        )
        embed.set_author(name="Membre banni", icon_url=f"{member.avatar_url}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"ID : {member.id}", icon_url=f"{self.bot.user.avatar_url}")
        await log_channel.send(embed=embed)

    @commands.command(
        description="Permet de supprimer un nombre de messages voulu"
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)
        await (await ctx.send(f"{amount} messages ont été supprimés")).delete(delay=3)
        await asyncio.sleep(3)

    @commands.command(
        description="Pour débannir une personne"
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        with open("guildconfig.json", "r") as f:
            chan = json.load(f)
        logchannel = chan[str(ctx.guild.id)]["logs"]
        log_channel = self.bot.get_channel(logchannel)

        userName, userId = member.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
            user = i.user
            if i.user.name == userName and i.user.discriminator == userId:
                await ctx.guild.unban(i.user)
                await ctx.send(f"{user.mention} a été unban")
                embed = discord.Embed(
                    color=0xCE2029, description=f"**{ctx.author.mention}** a unban **{user}**"
                )
                embed.set_author(name="Membre Débanni", icon_url=f"{user.avatar_url}")
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_thumbnail(url=f"{user.avatar_url}")
                embed.set_footer(text=f"ID : {user.id}", icon_url=f"{self.bot.user.avatar_url}")
                await log_channel.send(embed=embed)
                return

        await ctx.send(f"L'utilisateur {member} n'est pas dans la liste des personnes banni du serveur")

    @commands.command(
        description="Pour mute les gens méchant"
    )
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        mutedRole = await getMutedRole(ctx)
        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(f"{member.mention} a été mute !")

        embed = discord.Embed(
            color=0xCE2029, description=f"**{ctx.author.name}** a mute {member.mention} \n\nRaison : {reason}"
        )
        embed.set_author(name="Membre Mute", icon_url=f"{member.avatar_url}")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"ID : {member.id}", icon_url=f"{self.bot.user.avatar_url}")
        channel = self.bot.get_channel(763789256069087274)
        await channel.send(embed=embed)

    @commands.command(
        description="Seulement pour les gentils"
    )
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        mutedRole = await getMutedRole(ctx)
        await member.remove_roles(mutedRole, reason=reason)
        await ctx.send(f"{member.mention} a été démute")

        embed = discord.Embed(
            color=0xCE2029, description=f"**{ctx.author.name}** a démute {member.mention} \n\nRaison : {reason}"
        )
        embed.set_author(name="Membre Unmute", icon_url=f"{member.avatar_url}")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"ID : {member.id}", icon_url=f"{self.bot.user.avatar_url}")
        channel = self.bot.get_channel(763789256069087274)
        await channel.send(embed=embed)




