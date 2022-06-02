import discord
import os
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands, tasks
import random
import sys
import traceback
import json
import datetime


def get_prefix(bot, message):
    with open("guildconfig.json", "r") as f:
        prefix = json.load(f)

    return prefix[str(message.guild.id)]["prefix"]


intents = Intents.all()

bot = commands.Bot(command_prefix=get_prefix, description="Bot de Saiqo", intents=intents, help_command=None)
status = [f"help",
          "Rocket League",
          "Trayte est nul",
          "Macron EXPLOSION",
          "Yes i am",
          "Je suis froncé",
          "Yes is a giroud"]


@bot.event
async def on_ready():
    print("Bot Ready !")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Saiqo's bot"), status=discord.Status.dnd)


@bot.event
async def on_guild_join(guild):
    await guild.create_text_channel(name="logs")
    channel = discord.utils.get(guild.channels, name="logs")
    channel_id = channel.id
    with open("guildconfig.json", "r") as f:
        prefix = json.load(f)

    with open("guildconfig.json", "w") as f:
        prefix[str(guild.id)] = {}
        prefix[str(guild.id)]["prefix"] = "*"
        prefix[str(guild.id)]["logs"] = channel_id
        prefix[str(guild.id)]["welcome"] = 0
        prefix[str(guild.id)]["goodbye"] = 0
        json.dump(prefix, f, sort_keys=True, indent=4, ensure_ascii=False)

    with open("commandes.json", "r") as f:
        cmd = json.load(f)
    with open("commandes.json", "w") as f:
        cmd[str(guild.id)] = {}
        json.dump(cmd, f, sort_keys=True, indent=4, ensure_ascii=False)

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            with open("guildconfig.json", "r") as f:
                pre = json.load(f)
            prefix = pre[str(guild.id)]["prefix"]
            embed = discord.Embed(
                color=0xCE2029, description="**Merci de m'avoir ajouté sur ce serveur !**",
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=f"{bot.user.name}", icon_url=f"{bot.user.avatar_url}")
            embed.add_field(name="Voici la liste des choses a mettre en place :",
                            value=f"Salon d'acceuil des membres :\n`{prefix}setwelcome` \nSalon de départ des membres :\n`{prefix}setgoodbye`\n Salon de logs :\n`{prefix}setlogs`")
            embed.add_field(name="Autres fonctionalités :",
                            value=f"Vous pouvez customiser le préfix d'appel du bot avec :\n`{prefix}changeprefix`")
            await channel.send(embed=embed)
        break


@bot.event
async def on_guild_remove(guild):
    with open("guildconfig.json", "r") as f:
        prefix = json.load(f)
    prefix.pop(str(guild.id))
    with open("guildconfig.json", "w") as f:
        json.dump(prefix, f, indent=4)

    with open("commandes.json", "r") as f:
        commande = json.load(f)
    commande.pop(str(guild.id))
    with open("commandes.json", "w") as f:
        json.dump(prefix, f, indent=4)


"""@tasks.loop(hours=12)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(activity=game)"""


@bot.event
async def on_member_join(member):
    with open("guildconfig.json", "r") as f:
        welcome = json.load(f)
    channel = welcome[str(member.guild.id)]["welcome"]
    welcome_channel = bot.get_channel(channel)
    if welcome_channel is not None:
        await welcome_channel.send(f"Bienvenue ! {member.mention}")
    else:
        pass


@bot.event
async def on_member_remove(member):
    with open("guildconfig.json", "r") as f:
        goodbye = json.load(f)
    channel = goodbye[str(member.guild.id)]["goodbye"]
    goodbye_channel = bot.get_channel(channel)
    if goodbye_channel is not None:
        await goodbye_channel.send(f"Bye {member.mention}")
    else:
        pass


@bot.event
async def on_message(msg):
    if bot.user.mentioned_in(msg) and msg.mention_everyone is False:
        await msg.channel.send(f"Mon prefix pour se serveur est : ")
    await bot.process_commands(msg)


@bot.check
def check_commands(ctx):
    with open("commandes.json", "r") as f:
        cmd = json.load(f)
    commande = cmd[str(ctx.guild.id)]
    if ctx.command.name in commande:
        raise commands.DisabledCommand
    else:
        return True


@bot.event
async def on_command_error(ctx, error):
    with open("guildconfig.json", "r") as f:
        pre = json.load(f)
    prefix = pre[str(ctx.guild.id)]["prefix"]
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            f"Désolé mais cette commande n'existe pas ! \nTapez** {prefix}help ** pour voir la liste des commandes disponibles sur le serveur")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions pour faire cette commande !")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Oups ... Vous ne pouvez pas utiliser cette commande !")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument !")
    if isinstance(error, commands.DisabledCommand):
        await ctx.send("Cette commande est désactivé")
    if isinstance(error, discord.Forbidden):
        await ctx.send("Désolé, je n'ai pas les permissions nécéssaires pour faire cette commande !")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Argument invalide !")

    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


# Commandes ------------------------------------------------------------------------------------------------------------

def random_color():
    hexa = "123456789abcdef"
    random_hex = "0x"
    for i in range(6):
        random_hex += random.choice(hexa)
    return discord.Colour(int(random_hex, 16))


for file in os.listdir("cogs"):
    if file.endswith(".py") and not file.startswith("_"):
        print(f"cogs\{file[:-3]} loaded")
        bot.load_extension(f"cogs.{file[:-3]}")

load_dotenv()
token = os.getenv("SECRET")
bot.run(token)
