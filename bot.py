import discord
from discord.ext import commands
import os
from databases.DBConnection import *
from databases.SheetConnection import *
from dotenv import load_dotenv
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="-", intents=intents)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        # Ignorar __init__.py
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f'Error al cargar {filename}: {e}')


@bot.event
async def on_ready():
    print(f"¡Bot conectado como {bot.user}!")


async def main():
    bot.connectionBBDD = connectDB()
    bot.connectionExcel = connectSheet()
    async with bot:
        load_dotenv()
        await load_cogs()
        await bot.start(os.getenv("BOT_TOKEN"))

asyncio.run(main())