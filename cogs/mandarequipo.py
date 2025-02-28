import discord
from discord.ext import commands

class EquipoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.match_data = []

    @commands.command()
    async def mandarequipo(self, ctx): #This command is used in order for two players to send text (their teams) at the same time without
        # a middleman or external tools. Specifically designed for open teams tournaments.

        await ctx.author.send("Escribe el ID de Discord del usuario al que quieres enviar tu equipo:")

        def check_id(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        try:
            id_msg = await self.bot.wait_for('message', check=check_id, timeout=60.0)
            rival_id = id_msg.content.strip()

            try:
                rival = await self.bot.fetch_user(int(rival_id))
            except ValueError:
                await ctx.author.send("El ID proporcionado no es válido. Intenta nuevamente.") #Wrong ID format
                return
            except discord.NotFound:
                await ctx.author.send("No se encontró un usuario con ese ID. Verifica y vuelve a intentarlo.") #No user found
                return

            #Text to send, must start with "Equipo: "
            await ctx.author.send(f"Perfecto. Ahora escribe el texto que deseas enviar a {rival.name}, asegurándote de que empiece con 'Equipo:'")

            def check_text(message):
                return (
                    message.author == ctx.author
                    and isinstance(message.channel, discord.DMChannel)
                    and message.content.startswith("Equipo:")
                )

            text_msg = await self.bot.wait_for('message', check=check_text, timeout=60.0)
            text_to_send = text_msg.content[len("Equipo:"):].strip()

                #Bot stores User A, User B and the message the former wants to send to the latter.
            self.match_data.append([ctx.author.id, int(rival_id), text_to_send])
            await ctx.author.send(f"Datos guardados. Esperando que {rival.name} use el comando para completar el intercambio.")

            #Checks if User B has already tried to send a message to User A. If that's the case, both messages are sent. 
            for data in self.match_data:
                if data[0] == int(rival_id) and data[1] == ctx.author.id:
                    rival_text = data[2]
                    await ctx.author.send(f"{rival.name} te envió este mensaje: '{rival_text}'")
                    await rival.send(f"{ctx.author.name} te envió este mensaje: '{text_to_send}'")

                    self.match_data.remove(data)
                    self.match_data.remove([ctx.author.id, int(rival_id), text_to_send])

                    await ctx.author.send("El intercambio se ha completado exitosamente.")
                    await rival.send("El intercambio se ha completado exitosamente.")
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