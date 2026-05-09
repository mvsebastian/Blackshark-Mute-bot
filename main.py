import discord
from flask import Flask
from threading import Thread
import os

TOKEN = os.getenv("TOKEN")

GUILD_ID = 1385264203719377037
USER_ID = 611092749088849921

app = Flask('')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@app.route('/toggle')
def toggle():

    async def do_toggle():

        guild = client.get_guild(GUILD_ID)

        if guild is None:
            return

        member = guild.get_member(USER_ID)

        if member is None:
            return

        muted_role = discord.utils.get(guild.roles, name="Muted")

        if muted_role is None:
            return

        if muted_role in member.roles:
            await member.remove_roles(muted_role)
        else:
            await member.add_roles(muted_role)

    client.loop.create_task(do_toggle())

    return "DONE"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

@client.event
async def on_ready():
    print(f'Bot online: {client.user}')

keep_alive()
client.run(TOKEN)
