import discord
from discord.ext import commands
from aiohttp import request
import googletrans
import datetime
import json


def setup(bot):
    bot.add_cog(API(bot))


class API(commands.Cog):
    """Liste de commandes utilisant différentes API"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Pour traduire un mot / une phrase dans une langue shouaité", aliases=["tr"])
    async def translate(self, ctx, lang, *args):
        lang = lang.lower()
        if lang not in googletrans.LANGUAGES and lang not in googletrans.LANGCODES:
            await ctx.send("Langue invalide")
        text = " ".join(args)
        translator = googletrans.Translator()
        text_translated = translator.translate(text, dest=lang).text
        await ctx.send(text_translated)

    @commands.command(
        description="Liste des langues à traduires disponibles"
    )
    async def listelangue(self, ctx):
        a = googletrans.LANGUAGES
        test = ""
        for cle, value in a.items():
            test += f"{cle} - {value}\n"
        val1 = test[:724]
        val2 = test[724:]
        embed = discord.Embed(title="Liste des langues à traduires disponibles", color=0xCE2029)
        embed.add_field(name="1", value=val1)
        embed.add_field(name="2", value=val2, inline=True)
        embed.set_author(name=f"{self.bot.user.name}", icon_url=f"{self.bot.user.avatar_url}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(
        name="image",
        description="Envoie une image aléatoire d'un animal chosi parmis cette liste :\n*dog, cat, panda, fox, bird, koala, red_panda*"
    )
    async def image_animal(self, ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala", "red_panda"):
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None
                if image_link is not None:
                    await ctx.send(image_link)
                else:
                    await ctx.send("Pas d'images disponibles")

        else:
            await ctx.send("Pas d'images disponibles pour cette animal")

    @commands.command(description="Meme aléatoire")
    async def meme(self, ctx):
        URL = "https://some-random-api.ml/meme"
        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                meme_link = data["image"]
                test = data["caption"]
            else:
                meme_link = None
            if meme_link is not None:
                await ctx.send(meme_link)
                await ctx.send(test)

    @commands.command(description="Obtenir les jours fériés dans une année shouaité",
                      aliases=["jour_ferie", "jferie", "jf"])
    async def j_ferie(self, ctx, annee: int):
        url = f"https://calendrier.api.gouv.fr/jours-feries/metropole/{annee}.json"
        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                embed = discord.Embed(title=f"Jours fériés en France {annee}", color=0xCE2029)
                result = ""
                for key in data:
                    result += f"**{data[key]}** : {key} \n"

                embed.add_field(name=f"Dates :", value=f"{result}", inline=True)

        await ctx.send(embed=embed)

    @commands.command(description="Obtenir une photo du jour prise par la Nasa")
    async def apod(self, ctx):
        with open('secret.json', 'r') as secret_file:
            secret = json.load(secret_file)
        api_key = secret['nasa_api_key']
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                pic = data["url"]
                await ctx.send("Astronomy picture of the day :")
                await ctx.send(pic)
