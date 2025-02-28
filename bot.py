import discord
from discord.ext import commands
import os
from databases.DBConnection import *
from databases.SheetConnection import *
from dotenv import load_dotenv

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
    connectionBBDD=connectDB()
    if connectionBBDD:
        print(f"El bot se ha conectado a la base de datos {config['database']}")
    else:
        print(f"Error al conectarse a la base de datos {config['database']}")
    
    connectionExcel=connectSheet()
    if connectionExcel:
        print(f"El bot se ha conectado a la hoja de cálculo {sheetName}")
    else:
        print(f"Error al conectarse a la hoja de cálculo {sheetName}")
    

async def main():
    bot.connectionBBDD = connectDB()
    bot.connectionExcel = connectSheet()
    async with bot:
        load_dotenv()
        await load_cogs()
        await bot.start(os.getenv("BOT_TOKEN"))


# Iniciar el bot
import asyncio
asyncio.run(main())

