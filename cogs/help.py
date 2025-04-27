import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(name="help", aliases=["ayuda"], help="Help command that lists all the commands", brief="Utility")
    async def help_command(self, ctx, *, command_name: str = None):
        embed = discord.Embed(color=discord.Color.blue())

        if command_name is None:
            embed.title = "📖 Bot Manual"
            embed.description = "Here’s a list of available commands:"

            categorized_commands = {
                "Cards": [],
                "Users": [],
                "Utility": [],
                "Other": [],
                "Useless": []
            }

            for command in self.bot.commands:
                if command.hidden:
                    continue  # Skip hidden/internal commands

                category = command.brief or "Useless."
                command_name = f"`-{command.name}`"
                categorized_commands.setdefault(category, []).append(command_name)

            for command_list in categorized_commands.values():
                command_list.sort()
            if categorized_commands["Cards"]:
                embed.add_field(name=":joker: Cards Commands", value=" ".join(categorized_commands["Cards"]), inline=False)
            if categorized_commands["Users"]:
                embed.add_field(name=":mag_right: Users Commands", value=" ".join(categorized_commands["Users"]), inline=False)
            if categorized_commands["Utility"]:
                embed.add_field(name=":gear: Utility Commands", value=" ".join(categorized_commands["Utility"]), inline=False)
            if categorized_commands["Other"]:
                embed.add_field(name=":package: Other", value=" ".join(categorized_commands["Other"]), inline=False)

            embed.set_footer(text="Type `-help [command]` to get detailed info about a specific command.")
        else:
            command = self.bot.get_command(command_name.lower())
            if command:
                embed.title = f":information_source: Help: `{command.name}`"
                embed.description = command.help or "No description available."
            else:
                embed.title = ":x: Command Not Found"
                embed.description = f"No help available for `{command_name}`."

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
