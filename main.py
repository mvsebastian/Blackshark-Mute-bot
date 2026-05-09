import discord
import os

TOKEN = os.getenv("TOKEN")

GUILD_ID = 1385264203719377037
USER_ID = 611092749088849921
ROLE_ID = 1502766063467626647

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Bot online: {client.user}")


async def toggle_mute():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print("Guild not found")
        return

    member = guild.get_member(USER_ID)
    if member is None:
        print("User not found")
        return

    role = guild.get_role(ROLE_ID)
    if role is None:
        print("Role not found")
        return

    if role in member.roles:
        await member.remove_roles(role)
        print("Unmuted user")
    else:
        await member.add_roles(role)
        print("Muted user")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Stream Deck Lösung (über Discord Nachricht)
    if message.content == "!togglemute":
        await toggle_mute()


client.run(TOKEN)
