from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases=["pong"], help="Tests if the bot is working. Aliases: pong.", brief="Utility")
    async def ping(self, ctx):
        await ctx.send("¡Pong!")
        
async def setup(bot):
    await bot.add_cog(PingCog(bot))
