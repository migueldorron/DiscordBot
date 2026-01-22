import discord
import databases.pokesSSB
from discord.ext import commands
import aiohttp

class SSBCog(commands.Cog):
    listaPokemon=databases.pokesSSB.listaPokemon
    formatos=databases.pokesSSB.formatos
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        await self.session.close()

    @commands.command()
    async def puntos(self, ctx, *, input_pokemon):
        try:
            nombres = [nombre.strip() for nombre in input_pokemon.split("/")]

            if len(nombres) > 6:
                await ctx.send("Copiaste mal el team preview. Demasiados elementos.")
                return
            
            listaPokemon_lower = {k.lower(): v for k, v in self.listaPokemon.items()}
            sumaEquipo=0
            rangosEquipo=""

            for pokemon in nombres:
                pokemon_lower=pokemon.lower()
                if pokemon_lower in listaPokemon_lower:
                    datos = listaPokemon_lower[pokemon_lower]
                    sumaEquipo += datos[1]
                    rangosEquipo += datos[0] + " "
                else:
                    await ctx.send("Uno de los Pokemon no existe. Revisa si has copiado bien el team preview.")
                    return

            await ctx.send(f"Rangos: {rangosEquipo} \nSuma de puntos: {sumaEquipo}")

        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.command()
    async def tiers(self, ctx, *, input_pokemon):
        try:
            nombres = [nombre.strip() for nombre in input_pokemon.split("/")]

            if len(nombres) > 6:
                await ctx.send("Copiaste mal el team preview. Demasiados elementos.")
                return
            
            listaPokemon_lower = {k.lower(): v for k, v in self.listaPokemon.items()}
            sumaEquipo=0
            rangosEquipo=""
            formatosPoke={}

            for pokemon in nombres:
                pokemon_lower=pokemon.lower()
                if pokemon_lower in listaPokemon_lower:
                    datos = listaPokemon_lower[pokemon_lower]
                    sumaEquipo += datos[1]
                    rangosEquipo += datos[0] + " "
                    formatosPokeTemporal = datos[2:11] 
                    formatosPoke[pokemon] = formatosPokeTemporal

                else:
                    await ctx.send("Uno de los Pokemon no existe. Revisa si has copiado bien el team preview.")
                    return

            formatosValidos=[True] * 10

            for i in range(10):
                for poke in formatosPoke:
                    if not formatosPoke[poke][i]:
                        formatosValidos[i]=False
                        break

            listaFormatosValidos=[]
            for i, formato in enumerate(formatosValidos):
                if formato:
                    listaFormatosValidos.append(self.formatos[i])

            if listaFormatosValidos:
                await ctx.send(f"""Rangos: {rangosEquipo}
    Suma de puntos: {sumaEquipo}
    Tiers en las que se permite tu equipo: {listaFormatosValidos}""")
                
            else:
                await ctx.send("Tu equipo no es válido en ninguna tier lol.")

        except Exception as e:
            await ctx.send(f"Error: {e}")
                

    @commands.command()
    async def listatiers(self, ctx):
        await ctx.send(self.formatos)


    @commands.command()
    async def permitidos(self, ctx, tier: str):
        try:
            tier=tier.lower().replace(" ", "")
            self.formatos=[formato.lower().replace(" ","") for formato in self.formatos]

            indice = None

            for i in range(len(self.formatos)):
                if tier==self.formatos[i]:
                    indice=i
                    break
            
            if indice is not None:
                dictPermitidos={
                    "S":[],
                    "A+":[],
                    "A":[],
                    "A-":[],
                    "B+":[],
                    "B":[],
                    "B-":[],
                    "C+":[],
                    "C":[],
                    "C-":[],
                    "D":[]
                }

                for pokemon in self.listaPokemon:
                    if self.listaPokemon[pokemon][indice+2]:
                        dictPermitidos[self.listaPokemon[pokemon][0]].append(pokemon)

                mensajeFinal=""    
                for rango in dictPermitidos:
                    if dictPermitidos[rango]:
                        mensajeFinal += rango + ": `" + ", ".join(dictPermitidos[rango]) + "`\n"
                
                await ctx.send(mensajeFinal)

            else:
                await ctx.send(f"No se encuentra el formato. Aquí están todas las opciones. {self.formatos}")

        except Exception as e:
            await ctx.send(f"Error: {e}")
    
    @commands.command()
    async def crearequipo(self, ctx, *, input_pokemon):
        try:
            nombres = [nombre.strip() for nombre in input_pokemon.split("/")]

            if len(nombres) > 6:
                await ctx.send("Copiaste mal el team preview. Demasiados elementos.")
                return
            
            listaPokemon_lower = {k.lower(): v for k, v in self.listaPokemon.items()}


            lista_pokepastes=[]
            for pokemon in nombres:
                pokemon_lower=pokemon.lower()
                if pokemon_lower in listaPokemon_lower:
                    texto_pokepaste=await self.obtener_texto_pokepaste(listaPokemon_lower[pokemon_lower][12], self.session)
                    lista_pokepastes.append(texto_pokepaste)
            
            paste_final= await self.fusionarpastes(lista_pokepastes)

            await ctx.send(f"Equipo final: {paste_final}")

        except Exception as e:
            await ctx.send(f"Error: {e}")




    async def crear_pokepaste(self, texto, titulo):
        url = "https://pokepast.es/create"
        data = {
            "paste": texto,
            "title": titulo
        }
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/142.0.0.0 Safari/537.36"
            ),
            "Origin": "https://pokepast.es",
            "Referer": "https://pokepast.es/"
        }

        async with self.session.post(
            url,
            data=data,
            headers=headers,
            allow_redirects=False
        ) as resp:

            if resp.status != 303:
                text = await resp.text()
                raise Exception(f"Error creando paste: {resp.status} | {text}")

            location = resp.headers.get("Location")
            if not location:
                raise Exception("Pokepaste no devolvió Location header")

            return "https://pokepast.es" + location

    

    async def fusionarpastes(self, lista_pokepastes):
        equipo = "".join(lista_pokepastes)
        url_pokepaste = await self.crear_pokepaste(equipo, f"Equipo SSB")
        return url_pokepaste


    async def obtener_texto_pokepaste(self, url, session: aiohttp.ClientSession):
        headers = {"User-Agent": "Mozilla/5.0"}
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Error al obtener Poképaste RAW: {resp.status} | {text}")
            return await resp.text()
            

async def setup(bot):
    await bot.add_cog(SSBCog(bot))
