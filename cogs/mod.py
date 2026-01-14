import discord
from discord.ext import commands


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def banid(self, ctx, user_id: int, *, razon: str = "Unspecified reason"):
        try:
            if ctx.author.id!=438078850140864532:
                await ctx.send("You can't use that command")
                return
            
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.ban(user, reason=razon)

        except discord.NotFound:
            await ctx.send("User not found.")
        except discord.Forbidden:
            await ctx.send("I have no perms to ban that user..")
        except Exception as e:
            await ctx.send(f"Something unexpected happened: {e}")
        
async def setup(bot):
    await bot.add_cog(ModCog(bot))
