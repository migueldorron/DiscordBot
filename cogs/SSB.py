import discord
import databases.pokesSSB
from discord.ext import commands


class SSBCog(commands.Cog):
    listaPokemon=databases.pokesSSB.listaPokemon
    formatos=databases.pokesSSB.formatos
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def puntos(self, ctx, *, input_pokemon):

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

    @commands.command()
    async def tiers(self, ctx, *, input_pokemon):

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
                formatosPokeTemporal = datos[2:] 
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
        

    @commands.command()
    async def listatiers(self, ctx):
        await ctx.send(self.listatiers)


    @commands.command()
    async def permitidos(self, ctx, tier: str):

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
                   mensajeFinal += rango + ": " + ", ".join(dictPermitidos[rango]) + "\n"
            
            await ctx.send(mensajeFinal)

        else:
            await ctx.send(f"No se encuentra el formato. Aquí están todas las opciones. {self.formatos}")


async def setup(bot):
    await bot.add_cog(SSBCog(bot))
