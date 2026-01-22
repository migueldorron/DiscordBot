import discord
from discord.ext import commands
from datetime import date
import unicodedata
import json
from dotenv import load_dotenv
import os
import io

load_dotenv()
backup = int(os.getenv("SEND_ID"))

#Different commands I tried using while I was learning both Python and the Discord library. Uploaded just for information purposes.
class MiscelaneoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cartas_message_id = 1330148084952465429
        self.cartas_channel_id = 1318194896879882253
        self.awards_channel_id = 1463153281475022972
        
    @commands.command()
    async def editarmensaje(self, ctx, *, texto:str):
        canal = self.bot.get_channel(self.cartas_channel_id)
        mensaje = await canal.fetch_message(self.cartas_message_id)
        await mensaje.edit(content=texto)
        await ctx.send("Editado correctamente")
        return


    @commands.command()
    async def unicode(self, ctx, *, palabra: str):
        palabra_unicode=unicodedata.normalize('NFKD', palabra.lower())
        palabra_final=''.join([char for char in palabra_unicode if not unicodedata.combining(char)]) 
        await ctx.send(palabra_final)

    @commands.command()
    async def separar(self, ctx, args: str):
        argsList= [arg.strip() for arg in args.split(',')]
        for arg in argsList:
            await ctx.send(arg)

    @commands.command()
    async def testeo(self, ctx):
            await ctx.send("Testeo de ahora hecho: 1")        

    """@commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user or message.author.id==backup:
            return

        if isinstance(message.channel, discord.DMChannel):
            backup_send = await self.bot.fetch_user(backup)

            await backup_send.send(
                f"**Message**\n"
                f"**User:** {message.author} ({message.author.id})\n"
                f"**Content:** {message.content}"
            )

            for attachment in message.attachments:
                await backup_send.send(attachment.url)"""

    @commands.command()
    async def send(self, ctx, *, mensaje: str):
        if ctx.author.id != 438078850140864532:
            await ctx.send("Dónde vas calamar.")
            return
        await ctx.send(mensaje)    

    @commands.command()
    async def ordenarjson(self, ctx, *, json_texto):
        try:
            datos=json.loads(json_texto)

            if not isinstance(datos, dict):
                await ctx.send("Not a JSON.")
                return
                        
            json_ordenado = dict(
                sorted(datos.items(), key=lambda item: item[1], reverse=True)
                )
           
            await ctx.send(f"```json\n{json.dumps(json_ordenado, indent=2)}\n```")

        except json.JSONDecodeError:
            await ctx.send("Invalid JSON.")


    @commands.command()
    async def ordenarjson(self, ctx, *, json_texto=None):
        try:
            if ctx.message.attachments:
                archivo = ctx.message.attachments[0]
                contenido = await archivo.read()
                texto = contenido.decode("utf-8")
            else:
                if json_texto is None:
                    await ctx.send("Send a JSON either by text or attach a .txt file")
                    return
                texto = json_texto

            datos = json.loads(texto)

            if not isinstance(datos, dict):
                await ctx.send("Not a JSON.")
                return

            json_ordenado = dict(
                sorted(datos.items(), key=lambda item: item[1], reverse=True)
            )

            resultado = json.dumps(json_ordenado, indent=2, ensure_ascii=False)

            archivo_salida = io.BytesIO(resultado.encode("utf-8"))
            archivo_salida.seek(0)

            await ctx.send(
                file=discord.File(archivo_salida, filename="json.txt")
            )

        except json.JSONDecodeError:
            await ctx.send("Invalid JSON.")


    @commands.command()
    async def mandarcategoria(self, ctx, *, categoria: str):
        try:
            blacklist=[294523943514013701]
            if ctx.author.id in blacklist:
                ctx.send("Estás baneado de mandar sugerencias.")
                return
            
            canal = self.bot.get_channel(self.awards_channel_id)

            if canal is None:
                await ctx.send("No se pudo encontrar el canal de destino. Menciona a Dorron para que lo solucione.")
                return

            await canal.send(f"Sugerencia de <@{ctx.author.id}>: {categoria}")
            await ctx.send("Mensaje enviado.")

        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(MiscelaneoCog(bot))
