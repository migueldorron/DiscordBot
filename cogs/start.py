import discord
from discord.ext import commands

class StartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(name="start", help="Gives a quick guide about the bot and its purpose.", brief="Utility")
    async def help_command(self, ctx):
        embed = discord.Embed(color=discord.Color.blue())

    @commands.command(name="start", help="Gives a quick guide about the bot and its purpose.", brief="Utility")
    async def start_command(self, ctx):
        embed = discord.Embed(
            title="👋 Welcome to DorronBot!",
            description=(
                "Greetings! This is **DorronBot**, a Discord bot made by the user **Dorron** "
                "(<@438078850140864532>).\n\n"
                "The bot’s main purpose is to manage a **Google Sheet** to help you find other people "
                "to trade your cards with in **Pokémon Trading Card Game Pocket**.\n\n"
                "Since this is still a small bot, **please contact me before adding it to your server**, "
                "so I can help set everything up! It should only take a few minutes, and I’ll be glad to assist. \n\n"
                "To see all available commands, just type `-help`."
            ),
            color=discord.Color.gold()
        )
        embed.set_footer(text="Made with ❤️ by Dorron • Happy trading!")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(StartCog(bot))
