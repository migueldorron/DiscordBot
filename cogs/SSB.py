import discord
import databases.pokesSSB
from discord.ext import commands


class SSBCog(commands.Cog):
    listaPokemon=databases.pokesSSB.lista
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def puntos(self, ctx, *, input_pokemon):
        """
        Verifica la validez de un equipo de 6 Pokémon ingresados como un único string.
        Calcula la suma de puntos del equipo.
        """
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

        await ctx.send(f"Equipo mandado: {input_pokemon} \n Rangos: {rangosEquipo} \n Suma de puntos: {sumaEquipo}")

async def setup(bot):
    await bot.add_cog(SSBCog(bot))
