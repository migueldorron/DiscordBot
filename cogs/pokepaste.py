import discord
from discord.ext import commands
from gspread.utils import rowcol_to_a1
from collections import defaultdict
import requests
import re

class pokepasteCog(commands.Cog):
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection
        self.ssb_channel_id = 1445123970784301218
        self.ssb_mensaje_id = 1448442459246952538

    @commands.command()
    async def aprobado(self, ctx, *, texto_adicional: str):
        try:
            canal = self.bot.get_channel(self.ssb_channel_id)
            mensaje = await canal.fetch_message(self.ssb_mensaje_id)
            pokepaste = mensaje.content[-36:]
            texto_original = self.obtener_pokepaste_raw(pokepaste)
            pokepaste_adicional_url = self.crear_pokepaste(texto_adicional, titulo="Texto adicional")
            texto_adicional_raw = self.obtener_pokepaste_raw(pokepaste_adicional_url)
            textos=[texto_original, texto_adicional_raw]
            texto_final = "\n\n".join(textos)
            nueva_url = self.crear_pokepaste(texto_final, titulo="Pokemon SSB ENDLESS 9ARADOX")
            await mensaje.edit(content="TODOS LOS APROBADOS: " + nueva_url)
            await ctx.send(f"Mensaje actualizado correctamente: {nueva_url}")

        except Exception as e:
            await ctx.send(f"Hubo un error: {e}")

    @commands.command()
    async def setpokepaste(self, ctx, *, nuevo_contenido: str):
        try:    
            canal = self.bot.get_channel(self.ssb_channel_id)
            mensaje = await canal.fetch_message(self.ssb_mensaje_id)
            match = re.search(r"https?://pokepast\.es/([a-z0-9]{16})", nuevo_contenido)

            if match:
                url_final = f"https://pokepast.es/{match.group(1)}"
            else:
                url_final = self.crear_pokepaste(nuevo_contenido, titulo="Pokemon SSB ENDLESS 9ARADOX")
            await mensaje.edit(content="TODOS LOS APROBADOS: " + url_final)
            await ctx.send(f"Mensaje actualizado correctamente: {url_final}")

        except Exception as e:
            await ctx.send(f"Hubo un error al editar el mensaje: {e}")


    def obtener_pokepaste_raw(self, url):
        if not url.endswith("/raw"):
            url_raw = url + "/raw" if not url.endswith("/") else url + "raw"

        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url_raw, headers=headers)
        if r.status_code != 200:
            raise Exception(f"Error al obtener Poképaste RAW: {r.status_code}")
        return r.text
    
    def crear_pokepaste(self, texto, titulo):
        url = "https://pokepast.es/create"
        data = {"paste": texto, "title": titulo}
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://pokepast.es",
            "Referer": "https://pokepast.es/",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        r = requests.post(url, data=data, headers=headers, allow_redirects=False)
        if r.status_code != 303:
            raise Exception(f"Error creando paste: {r.status_code}")
        return "https://pokepast.es" + r.headers["Location"]
    

        
async def setup(bot):
    from databases.SheetConnection import connectSheet
    await bot.add_cog(pokepasteCog(bot, connectSheet))