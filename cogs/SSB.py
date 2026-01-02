import discord
from discord.ext import commands
import os


#Different commands I tried using while I was learning both Python and the Discord library. Uploaded just for information purposes.
class MiscelaneoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verificar(self, ctx, input_pokemon, df):
        """
        Verifica la validez de un equipo de 6 Pokémon ingresados como un único string.
        Calcula la suma de puntos del equipo.
        """
        # Dividir el input por el separador " / "
        nombres = input_pokemon.split(" / ")

        if len(nombres) != 6:
            await ctx.send("Copiaste mal el team preview")

        # Buscar los Pokémon en el DataFrame
        equipo = df[df["Pokémon"].isin(nombres)]

        if len(equipo) != 6:
            return "Copiaste mal el team preview"

        # Calcular la suma de puntos
        suma_puntos = equipo["puntos"].sum()

        # Mostrar los detalles del equipo y la suma de puntos
        print("Equipo ingresado:")
        print(equipo[["Pokémon", "Rank", "puntos"]].to_string(index=False))
        return f"Suma total de puntos: {suma_puntos}"



    print("Ingresa los pokes como salen en el team preview\nEjemplo:\nGhostGius's team: \nTapu Koko / Garganacl / Tinkaton / Ursaluna-Bloodmoon / Marshadow / Eelektross-Mega")
    input_pokemon = input("Pega el team preview: \n")
    resultado = verificar_equipo(input_pokemon, dfrb)
    print(resultado)

async def setup(bot):
    await bot.add_cog(MiscelaneoCog(bot))
