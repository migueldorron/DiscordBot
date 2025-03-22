import discord
from discord.ext import commands
import databases.translations

class EquipoCog(commands.Cog):
    dict=databases.translations.mandarEquipoComandos
    def __init__(self, bot):
        self.bot = bot
        self.match_data = []

    @commands.command(name="mandarequipo", aliases=["sendteam"])
    async def mandarequipo(self, ctx): #This command is used in order for two players to send text (their teams) at the same time without
        # a middleman or external tools. Specifically designed for open teams tournaments.


        await ctx.author.send(self.dict[ctx.invoked_with][0])

        def check_id(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        try:
            id_msg = await self.bot.wait_for('message', check=check_id, timeout=60.0)
            rival_id = id_msg.content.strip()

            try:
                rival = await self.bot.fetch_user(int(rival_id))
            except ValueError:
                await ctx.author.send(self.dict[ctx.invoked_with][1]) #Wrong ID format
                return
            except discord.NotFound:
                await ctx.author.send(self.dict[ctx.invoked_with][2]) #No user found
                return

            #Text to send, must start with "Team: "
            await ctx.author.send(self.dict[ctx.invoked_with][3].format(rival_name="<@"+str(rival_id)+">"))

            def check_text(message):
                return (
                    message.author == ctx.author
                    and isinstance(message.channel, discord.DMChannel)
                    and message.content.startswith("Team:")
                )

            text_msg = await self.bot.wait_for('message', check=check_text, timeout=60.0)
            text_to_send = text_msg.content[len("Team:"):].strip()

                #Bot stores User A, User B and the message the former wants to send to the latter.
            self.match_data.append([ctx.author.id, int(rival_id), text_to_send])
            await ctx.author.send(self.dict[ctx.invoked_with][4].format(rival_name="<@"+str(rival_id)+">"))

            #Checks if User B has already tried to send a message to User A. If that's the case, both messages are sent. 
            for data in self.match_data:
                if data[0] == int(rival_id) and data[1] == ctx.author.id:
                    rival_text = data[2]
                    await ctx.author.send(f"{rival.name} -> '{rival_text}'")
                    await rival.send(f"{ctx.author.name} -> '{text_to_send}'")

                    self.match_data.remove(data)
                    self.match_data.remove([ctx.author.id, int(rival_id), text_to_send])

                    await ctx.author.send(":handshake:")
                    await rival.send(":handshake:")
                    break

        #Multiple exceptions
        except discord.errors.Forbidden:
            await ctx.author.send("No puedo enviar mensajes a ese usuario. Asegúrate de que permita mensajes directos.")
        except TimeoutError:
            await ctx.author.send("No recibí respuesta a tiempo. El proceso ha sido cancelado.")
        except Exception as e:
            await ctx.author.send(f"Ha ocurrido un error inesperado: {str(e)}")


async def setup(bot):
    await bot.add_cog(EquipoCog(bot))