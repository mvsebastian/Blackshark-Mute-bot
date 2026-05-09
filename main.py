import discord
from flask import Flask
import os
import asyncio
import threading

TOKEN = os.getenv("TOKEN")

GUILD_ID = 1385264203719377037
USER_ID = 611092749088849921

app = Flask(__name__)

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# wird später gesetzt wenn Bot ready ist
loop = None


@app.route("/")
def home():
    return "Bot is running"


@app.route("/toggle")
def toggle():
    if loop is None:
        return "Bot not ready"

    asyncio.run_coroutine_threadsafe(toggle_role(), loop)
    return "OK"


async def toggle_role():
    await client.wait_until_ready()

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
    global loop
    loop = asyncio.get_running_loop()
    print(f"Bot online: {client.user}")


def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


threading.Thread(target=run_web).start()

client.run(TOKEN)
