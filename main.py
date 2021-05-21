import discord
import os
import requests
import asyncio
import psycopg2
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt=f"%m/%d/%Y %H:%M:%S %Z")
logger = logging.getLogger("Snipe Bot")


client = commands.Bot(command_prefix=".")
scheduler = AsyncIOScheduler()

DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

with conn:
    # cur.execute("CREATE TABLE coursesToBeFound (index VARCHAR primary key);")
    cur.execute("INSERT INTO coursesToBeFound (index) VALUES (%s)", ("00150",))
    # cur.execute("DELETE FROM coursesToBeFound where index = %s", ("00150",))
    # cur.execute("SELECT * from coursesToBeFound;")
    # for row in cur:
    #     print(row[0])

sectionsFound = []

@client.event
async def on_ready():
    logger.info("Bot is ready")

@client.command()
async def addCourse(ctx, arg):
    logger.info(arg)
    await ctx.send("Successfully Added the Course to Snipe!")

    with conn:
        cur.execute("INSERT INTO coursesToBeFound (index) VALUES (%s)", (arg,))

async def check_courses():
    url = "https://sis.rutgers.edu/soc/api/openSections.json?year=2021&term=9&campus=NB"

    try:
        dataJSON = requests.get(url).json()
    except Exception as e:
        logger.info(e)

        return

    cur.execute("SELECT * from coursesToBeFound;")

    for row in cur:
        logger.info(row)
        for index in dataJSON:
            if row[0] == index:
                sectionsFound.append(index)
                logger.info(f"Found index: {row[0]}")
                await client.get_channel(841918517972172804).send(f"Found Index: {index}")


    for index in sectionsFound:
        cur.execute("DELETE FROM coursesToBeFound where index = %s", (index,))
        conn.commit()

if __name__ == "__main__":
    logger.info("Starting")
    scheduler.add_job(check_courses, "interval", seconds=10)
    scheduler.start()
    client.run(os.environ.get("token"))
