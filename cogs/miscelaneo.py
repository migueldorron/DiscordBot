import discord
from discord.ext import commands
from datetime import date
import unicodedata

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

    @commands.command()
    async def on_message(self, ctx, message):

    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        receptor = await bot.fetch_user(RECEPTOR_ID)
        # Enviamos el contenido con info del autor original
        await receptor.send(
            f"📩 **Nuevo mensaje privado recibido**\n"
            f"**Usuario:** {message.author} ({message.author.id})\n"
            f"**Contenido:** {message.content}"
        )
       
async def setup(bot):
    await bot.add_cog(MiscelaneoCog(bot))
