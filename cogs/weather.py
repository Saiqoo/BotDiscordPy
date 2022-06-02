import discord
from discord.ext import commands
import json
import requests
from aiohttp import request

with open('secret.json', 'r') as secret_file:
    secret = json.load(secret_file)
api_key = secret['weather_api_key']


def setup(bot):
    bot.add_cog(Weather(bot))


def get_meteo_icon(meteo, is_day):
    if is_day == 1:
        if meteo == "Ensoleillé":
            return ":sunny:"
        if meteo == "Partiellement nuageux":
            return ":white_sun_small_cloud:"
        if meteo == "Nuageux" or meteo == "Couvert":
            return ":cloud:"
        if meteo == "Brume" or meteo == "Brouillard" or meteo == "Brouillard givrant":
            return "<:mist:847475391686115333>"
        if meteo == "Pluie éparse à proximité" or meteo == "Pluie légère éparse" or meteo == "Pluie modérée par moments" or meteo == "Pluie forte par moments" or meteo == "Averse de pluie légère" or meteo == "Averse de pluie modérée":
            return ":white_sun_rain_cloud:"
        if meteo == "Neige éparse à proximité" or meteo == "Neige légère éparse" or meteo == "Neige modérée éparse" or meteo == "Neige forte éparse" or meteo == "Légères averses de neige":
            return "<:patchy_snow:847475846502809630>"
        if meteo == "Grésil épars à proximité" or meteo == "Léger grésil" or meteo == "Grésil modéré à fort" or meteo == "Légères averses de grésil" or meteo == "Averses de grésil modérées à fortes":
            return "<:patchy_sleet:847482488850612284>"
        if meteo == "Foyers orageux à proximité" or meteo == "Pluie forte à modérée avec tonerre par endroit" or meteo == "Neige éparse modérée à forte avec tonnerre par endroit":
            return "<:rain_thunder:847492671509626911>"
        if meteo == "Rafales de neige" or meteo == "Blizzard" or meteo == "Neige forte":
            return "<:snow:847483947956830278>"
        if meteo == "Bruine légère éparse" or meteo == "Bruine légère":
            return "<:light_drizzle:847485797082726420>"
        if meteo == "Bruine verglaçante" or meteo == "Forte bruine verglaçante" or meteo == "Bruine verglaçante éparse à proximité" or meteo == "Pluie verglaçante légère" or meteo == "Pluie verglaçante modérée à forte":
            return "<:freezing_drizzle:847486332132524093>"
        if meteo == "Pluie légère" or meteo == "Pluie modérée" or meteo == "Pluie forte":
            return ":cloud_rain:"
        if meteo == "Neige légère" or meteo == "Neige modérée" or meteo == "Crystaux de glace" or meteo == "Averses de neige modérées à fortes" or meteo == "Légères averses de crystaux de glace" or meteo == "Averses de crystaux de glace modérées à fortes":
            return "<:light_snow:847490251454939157>"
        if meteo == "Averses de pluie torrentielle":
            return "<:rain_shower:847491538946752622>"
        if meteo == "Légère neige éparse avec tonnerre par endroit" or meteo == "Légère pluie éparse avec tonnerre par endroit":
            return "<:light_rain_thunder:847493792143769680>"
    if is_day == 0:
        return ":crescent_moon:"


class Weather(commands.Cog):
    """Liste de commandes utilisant différentes API"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Obtenir la météo actuelle", aliases=["météonow", "Météonow", "Meteonow", "NowMeteo", "nowmeteo"])
    async def meteonow(self, ctx, *location):
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=yes&lang=fr'
        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = json.loads(requests.get(url).content)

                city = data["location"]['name']
                meteo_icon = data["current"]["condition"]["icon"]
                country = data['location']['country']
                time = data['location']['localtime']
                wcond = data['current']['condition']['text']
                celcius = data['current']['temp_c']
                fclike = data['current']['feelslike_c']

                embed = discord.Embed(title=f"Météo {city}", description=f"{country}", color=0xCE2029)
                embed.set_thumbnail(url=f"http:{meteo_icon}")
                embed.add_field(name=":thermometer: Température :", value=f"{celcius} C°", inline=True)
                embed.add_field(name="Condition :", value=f"{wcond}", inline=False)
                embed.add_field(name=":man_standing: Ressenti :", value=f"{fclike} C°", inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Impossible de trouver cette ville")

    @commands.command(description="Obtenir la météo pour les prochains jours", aliases=["météo", "Météo", "Meteo"])
    async def meteo(self, ctx, day: int, *location):
        if day < 1 or day > 3:
            await ctx.send("Saisissez un nombre de jour entre 1 et 3")
        else:
            url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days={day}&aqi=no&alerts=no&lang=fr'
            async with request("GET", url, headers={}) as response:
                if response.status == 200:
                    data = json.loads(requests.get(url).content)

                    """Value per days"""
                    city = data["location"]['name']
                    country = data['location']['country']
                    date = data['forecast']['forecastday'][0]['date']

                    embed = discord.Embed(title=f"Météo {city}", description=f"{country}", color=0xCE2029)
                    for i in range(0, day):
                        value = ""
                        for y in range(0, 12):
                            hour = f"{y}:00"
                            is_day = data["forecast"]["forecastday"][i]["hour"][y]["is_day"]
                            meteo = data["forecast"]["forecastday"][i]["hour"][y]["condition"]["text"]
                            emoji = get_meteo_icon(meteo, is_day)
                            value += f"{hour} : {emoji} \n"

                        embed.add_field(name="\u200b", value=f"{value}", inline=True)
                        value = ""

                        for y in range(12, 24):
                            hour = f"{y}:00"
                            is_day = data["forecast"]["forecastday"][i]["hour"][y]["is_day"]
                            meteo = data["forecast"]["forecastday"][i]["hour"][y]["condition"]["text"]
                            emoji = get_meteo_icon(meteo, is_day)
                            value += f"{hour} : {emoji} \n"

                        max_temp = str(data['forecast']['forecastday'][i]['day']['maxtemp_c']) + " C°"
                        min_temp = str(data['forecast']['forecastday'][i]['day']['mintemp_c']) + " C°"
                        avg_humidity = str(data['forecast']['forecastday'][i]['day']['avghumidity']) + " %"
                        chance_of_rain = str(data['forecast']['forecastday'][i]['day']['daily_chance_of_rain']) + " %"
                        sunrise = str(data['forecast']['forecastday'][i]['astro']['sunrise'])
                        sunset = str(data['forecast']['forecastday'][i]['astro']['sunset'])
                        day_info = f"\u200b\n\u200b\n\u200b\n:thermometer: Max : {max_temp} \n:thermometer: Min : {min_temp} \n:sweat_drops: : {avg_humidity} \n:cloud_rain: : {chance_of_rain} \n:sunrise_over_mountains: : {sunrise} \n:city_sunset: : {sunset} "

                        embed.add_field(name=f"{date}", value=f"{value}", inline=True)
                        embed.add_field(name="\u200b", value=f"{day_info}", inline=True)
                        embed.add_field(name="\u200b", value="\u200b", inline=False)

            await ctx.send(embed=embed)
