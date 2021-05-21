import discord
import os
import requests
import asyncio
import psycopg2

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

client = commands.Bot(command_prefix=".")
scheduler = AsyncIOScheduler()

DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

# with conn:
    # cur.execute("CREATE TABLE coursesToBeFound (index VARCHAR primary key);")
    # cur.execute("INSERT INTO coursesToBeFound (index) VALUES (%s)", ("00150",))
    # cur.execute("DELETE FROM coursesToBeFound where index = %s", ("00150",))
    # cur.execute("SELECT * from coursesToBeFound;")
    # for row in cur:
    #     print(row[0])




sections = ["00149", "01212", "00150"]
sectionsFound = []

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def addCourse(ctx, arg):
    print(arg)
    sections.append(arg)
    await ctx.send("Successfully Added the Course to Snipe!")

    with conn:
        cur.execute("INSERT INTO coursesToBeFound (index) VALUES (%s)", (arg,))


    for course in sections:
        print(f"Courses: {course}")

# @scheduler.scheduled_job("interval", seconds=10)
async def check_courses():
    url = "https://sis.rutgers.edu/soc/api/openSections.json?year=2021&term=9&campus=NB"
    dataJSON = requests.get(url).json()

    cur.execute("SELECT * from coursesToBeFound;")

    for row in cur:
        print(row)
        for index in dataJSON:
            if row[0] == index:
                sectionsFound.append(index)
                print(f"Found index: {row[0]}")
                await client.get_channel(841918517972172804).send(f"Found Index: {index}")


    for index in sectionsFound:
        cur.execute("DELETE FROM coursesToBeFound where index = %s", (index,))
        conn.commit()

    # for course in sections:
    #     for index in dataJSON:
    #         if index == course:
    #             sectionsFound.append(index)
    #             print(f"Found: {index}")
    #             await client.get_channel(841918517972172804).send(f"Found Index: {index}")
    #
    #             sections.remove(index)

                # with conn:
                #     cur.execute("DELETE FROM coursesToBeFound where index = %s", (index,))

# cur.close()
# conn.close()

if __name__ == "__main__":
    print("Starting")
    scheduler.add_job(check_courses, "interval", seconds=10)
    scheduler.start()
    client.run(os.environ.get("token"))
