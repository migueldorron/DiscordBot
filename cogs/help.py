import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(name="help", aliases=["ayuda"])
    async def help_command(self, ctx, *, command_name: str = None):
        embed = discord.Embed(color=discord.Color.blue())

        if command_name is None:
            embed.title = "📖 Bot Manual"
            embed.description = "List of available commands:"

            embed.add_field(
                name="🃏 Trading Commands",
                value="`-tengocartas`, `-buscocartas`, `-tengocartasañadir`, `-buscocartasañadir`",
                inline=False
            )

            embed.add_field(
                name="🔎 Search Commands",
                value="`-buscarcarta`, `-buscarusuario`",
                inline=False
            )

            embed.add_field(
                name="⚙️ Utility",
                value="`-ping`, `-coin`",
                inline=False
            )

            embed.set_footer(text="Type `-help [command]` to get detailed info about a specific command.")
        else:
            command_name = command_name.lower()

            help_texts = {
                "tengocartas": "-tengocartas <cards>: Replace your cards for trade. Separate cards with '-'",
                "buscocartas": "-buscocartas <cards>: Replace your wanted cards. Separate cards with '-'",
                "tengocartasañadir": "-tengocartasañadir <cards>: Add cards to your trade list.",
                "buscocartasañadir": "-buscocartasañadir <cards>: Add cards to your wanted list.",
                "buscarcarta": "-buscarcarta <card>: Find users who have a specific card.",
                "buscarusuario": "-buscarusuario <user>[, rarity]: Find cards a user has, or filter by rarity.",
                "ping": "-ping: Check if the bot is alive.",
                "coin": "-coin: Flip a coin."
            }

            description = help_texts.get(command_name)

            if description:
                embed.title = f":information_source: Help: `{command_name}`"
                embed.description = description
            else:
                embed.title = ":x: Command Not Found"
                embed.description = f"No help available for `{command_name}`."

        await ctx.send(embed=embed)

        
async def setup(bot):
    await bot.add_cog(HelpCog(bot))
