import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))  

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True

keep_alive()

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print(f"Failed to find guild with ID {GUILD_ID}")
        return
    

    member_count = guild._member_count
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{member_count} members"
    ))  
async def load_commands():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"commands.{filename[:-3]}")

import asyncio
asyncio.run(load_commands())


bot.run(TOKEN, root_logger=True)
