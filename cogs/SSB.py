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

        nombres = input_pokemon.split(" / ")

        if len(nombres) > 6:
            await ctx.send("Copiaste mal el team preview. Demasiados elementos.")
            return

        sumaEquipo=0
        rangosEquipo=""
        for pokemon in nombres:
            if pokemon in self.listaPokemon:
                sumaEquipo+=self.listaPokemon[pokemon][1]
                rangosEquipo+=self.listaPokemon[pokemon][0]+" "
            else:
                await ctx.send("Uno de los Pokemon no existe. Revisa si has copiado bien el team preview.")
                return

        await ctx.send(f"Rangos: {rangosEquipo} \nSuma de puntos: {sumaEquipo}")

    @commands.command()
    async def tiers(self, ctx, *, input_pokemon):

        nombres = input_pokemon.split(" / ")

        if len(nombres) > 6:
            await ctx.send("Copiaste mal el team preview. Demasiados elementos.")
            return

        sumaEquipo=0
        rangosEquipo=""
        formatosPoke={}
        for pokemon in nombres:
            if pokemon in self.listaPokemon:
                sumaEquipo+=self.listaPokemon[pokemon][1]
                rangosEquipo+=self.listaPokemon[pokemon][0]+" "
                formatosPokeTemporal=self.listaPokemon[pokemon][2:]
                formatosPoke[pokemon]=formatosPokeTemporal
            else:
                await ctx.send("Uno de los Pokemon no existe. Revisa si has copiado bien el team preview.")
                return

        formatosValidos=[True] * 8

        for i in range(8):
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
        



async def setup(bot):
    await bot.add_cog(SSBCog(bot))
