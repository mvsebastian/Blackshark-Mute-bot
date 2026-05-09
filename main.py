import discord
from flask import Flask
import os
import asyncio
import threading
import time

TOKEN = os.getenv("TOKEN")

GUILD_ID = 1385264203719377037
USER_ID = 611092749088849921

app = Flask(__name__)

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

loop = None
ready_flag = False


@app.route("/")
def home():
    return "Bot is running"


@app.route("/toggle")
def toggle():
    global ready_flag, loop

    # kurze Wartezeit bis Bot ready ist
    timeout = 15
    waited = 0

    while not ready_flag and waited < timeout:
        time.sleep(0.5)
        waited += 0.5

    if not ready_flag or loop is None:
        return "Bot still starting, try again"

    asyncio.run_coroutine_threadsafe(toggle_role(), loop)
    return "OK"


async def toggle_role():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        return

    member = guild.get_member(USER_ID)
    if member is None:
        return

    role = discord.utils.get(guild.roles, name="Muted")
    if role is None:
        return

    if role in member.roles:
        await member.remove_roles(role)
    else:
        await member.add_roles(role)


@client.event
async def on_ready():
    global loop, ready_flag
    loop = asyncio.get_running_loop()
    ready_flag = True
    print(f"Bot online: {client.user}")


def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


threading.Thread(target=run_web).start()

client.run(TOKEN)
