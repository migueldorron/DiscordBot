import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
@commands.command(name="help")
async def help_command(self, ctx):
    embed = discord.Embed(title="Bot Manual 📖", description="Here's how to use the bot!", color=discord.Color.blue())
    
    embed.add_field(name="📦 Trading Commands", value="-tengocartas\n-buscocartas\n-buscarcarta\n", inline=False)
    embed.add_field(name="🎯 Other Commands", value="-buscarusuario\n-moneda\n-ping\n", inline=False)
    embed.set_footer(text="Bot created by Dorron - v1.0")

    await ctx.send(embed=embed)


       
async def setup(bot):
    await bot.add_cog(HelpCog(bot))
