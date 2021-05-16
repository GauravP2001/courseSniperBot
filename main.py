import discord
import os
import requests

from discord.ext import commands

client = commands.Bot(command_prefix=".")


@client.event
async def on_ready():
    print("Bot is ready")

url = "https://sis.rutgers.edu/soc/api/openSections.json?year=2021&term=9&campus=NB"
dataJSON = requests.get(url).json()

sections = ["00149", "01212", "00150"]
sectionsFound = []

for course in sections:
    for index in dataJSON:
        if index == course:
            sectionsFound.append(index)

for section in sectionsFound:
    print(section)



client.run(os.environ.get("token"))
