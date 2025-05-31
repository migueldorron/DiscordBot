import discord
from discord.ext import commands
import asyncio

class MessageDownloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def descargarChat(self, ctx):
        channel = ctx.channel
        
        if ctx.author.id != 438078850140864532:
            await ctx.send("Dónde vas calamar.")
            return
        
        filename="chat.txt"

        await ctx.send("Descargando papu.")
        with open(filename, "w", encoding="utf-8") as file:
            async for message in channel.history(limit=None, oldest_first=True):
                file.write(f"{message.author}: {message.content}\n")

        await ctx.author.send("Descargado papu.", file=discord.File(filename))

async def setup(bot):
    await bot.add_cog(MessageDownloadCog(bot))