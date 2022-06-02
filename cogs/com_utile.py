import discord
from discord.ext import commands
from pyfiglet import Figlet
from PIL import Image
from io import BytesIO
import binascii


def setup(bot):
    bot.add_cog(Fun(bot))


class Fun(commands.Cog):
    """Liste de commandes amusantes"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description="Change le texte que tu veux sous la forme ASCII"
    )
    async def render(self, ctx, *, msg):
        f = Figlet(font="big")
        g = "```" + f.renderText(msg) + "```"
        await ctx.send(g)

    @commands.command(
        description="Latence entre l'utilisateur et le bot"
    )
    async def ping(self, ctx):
        await ctx.send(f"Votre ping est : {round(self.bot.latency * 1000)} ms")

    @commands.command(
        description="Converti nombre / chaine de caractères en binaire"
    )
    async def texttobin(self, ctx, *, msg: str):
        bin_repr = lambda s, coding="ascii": ' '.join('{0:08b}'.format(c) for c in s.encode(coding))
        await ctx.send(bin_repr(msg))

    @commands.command(
        description="Obtenir l'image profile d'une membre"
    )
    async def pp(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(ctx.author.avatar_url)
        else:
            await ctx.send(member.avatar_url)

    @commands.command(
        description="Envoie un avis de recherche"
    )
    async def wanted(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        wanted = Image.open("image/wanted.png")
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((228, 228))
        wanted.paste(pfp, (117, 208))
        wanted.save("image/profile.png")
        await ctx.send(file=discord.File("image/profile.png"))

    @commands.command(
        description="Convertir du binaire vers du texte"
    )
    async def bintotext(self, ctx, *, msg: str):
        ascii_string = "".join([chr(int(binary, 2)) for binary in msg.split(" ")])
        await ctx.send(ascii_string)

    @commands.command(
        description="Convertir du texte en Hexadecimal"
    )
    async def texttohex(self, ctx, *, msg):
        encode = msg.encode('utf-8')
        hexadecimal = binascii.hexlify(encode)
        resultat = hexadecimal.decode('utf-8')
        await ctx.send(resultat)

    @commands.command(
        description="Convertir de l'Héxadécimal en texte"
    )
    async def hextotext(self, ctx, *, msg):
        valeur = binascii.unhexlify(msg)
        resultat = valeur.decode('utf-8')
        await ctx.send(resultat)
