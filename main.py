import discord
import os
import requests
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

client = commands.Bot(command_prefix=".")
scheduler = AsyncIOScheduler()

@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def send_message():
    channel = client.get_channel(841918517972172804)
    await channel.send('Index Found: ')

# @scheduler.scheduled_job("interval", seconds=10)
async def check_courses():
    url = "https://sis.rutgers.edu/soc/api/openSections.json?year=2021&term=9&campus=NB"
    dataJSON = requests.get(url).json()

    sections = ["00149", "01212", "00150"]
    sectionsFound = []

    for course in sections:
        for index in dataJSON:
            if index == course:
                sectionsFound.append(index)
                await client.get_channel(841918517972172804).send("Found Index: ")


    for section in sectionsFound:
        print(section)


if __name__ == "__main__":
    scheduler.add_job(check_courses, "interval", seconds=10)
    scheduler.start()
    client.run(os.environ.get("token"))
