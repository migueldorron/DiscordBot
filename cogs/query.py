import discord
from discord.ext import commands

class QueryCog(commands.Cog):
    def __init__(self, bot, connectionBBDD):
        self.bot = bot
        self.connectionBBDD = connectionBBDD  # Conexión pasada desde bot.py

    @commands.command(name="getusers")
    async def getusers(self, ctx):
        if not self.connectionBBDD:
            await ctx.send("Connection to the database failed.")
            return

        try:
            cursor = self.connectionBBDD.cursor()
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()

            if result:
                mensaje = "Users:\n"
                for user in result:
                    mensaje += f"ID: {user[0]}, Nombre: {user[1]}, Email: {user[2]}\n"
                await ctx.send(mensaje)
            else:
                await ctx.send("No users found in the database.")

        except Exception as e:
            await ctx.send(f"Query exception: {e}")
        finally:
            cursor.close()

async def setup(bot):
    connectionBBDD = bot.connectionBBDD
    await bot.add_cog(QueryCog(bot, connectionBBDD))
