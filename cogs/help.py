import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(name="help", aliases=["ayuda"])
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="📖 Bot Manual",
            description="Here’s how to use the Trading Bot!",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="🃏 Trading Commands",
            value=(
                "`-tengocartas <cards>` → Replace your card list for trading.\n"
                "`-buscocartas <cards>` → Replace your card list you are searching for.\n"
                "`-tengocartasañadir <cards>` → Add cards to your trading list.\n"
                "`-buscocartasañadir <cards>` → Add cards to your search list.\n"
            ),
            inline=False
        )

        embed.add_field(
            name="🔎 Search Commands",
            value=(
                "`-buscarcarta <card>` → Find users who have a specific card.\n"
                "`-buscarusuario <username>[, rarity]` → Find all cards or cards by rarity for a user.\n"
            ),
            inline=False
        )

        embed.add_field(
            name="⚙️ Utility",
            value=(
                "`-ping` → Check if the bot is alive.\n"
                "`-coin` → Flip a coin.\n"
            ),
            inline=False
        )

        embed.set_footer(text="Use commands exactly as shown. Separate multiple cards with '-' when needed.")
        
        await ctx.send(embed=embed)


       
async def setup(bot):
    await bot.add_cog(HelpCog(bot))
