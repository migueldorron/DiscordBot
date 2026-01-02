import discord
from discord.ext import commands
from datetime import date
import unicodedata
import json
from dotenv import load_dotenv
import os

load_dotenv()
backup = int(os.getenv("SEND_ID"))

#Different commands I tried using while I was learning both Python and the Discord library. Uploaded just for information purposes.
class MiscelaneoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cartas_message_id = 1330148084952465429
        self.cartas_channel_id = 1318194896879882253
        
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

    @commands.Cog.listener()
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
                await backup_send.send(attachment.url)

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
            ctx.send("1")
            if not isinstance(datos, dict):
                await ctx.send("Not a JSON.")
                return
            
            ctx.send("2")
            
            json_ordenado = dict(
                sorted(json.items(), key=lambda item: item[1], reverse=True)
                )
            
            ctx.send("3")
           
            await ctx.send(f"```json\n{json.dumps(json_ordenado, indent=2)}\n```")

        except json.JSONDecodeError:
            await ctx.send("Invalid JSON.")

async def setup(bot):
    await bot.add_cog(MiscelaneoCog(bot))
