from discord.ext import commands

class cardsCog(commands.Cog):
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection

    @commands.command()
    async def tengocartas(self, ctx, *, new_cards: str): # Replaces existing text in cells
        try:
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("TCG_Tengo")

            # Checking if the user already exists in the sheet
            existing_rows = sheet.get_all_values()
            user_row = None

            for index, row in enumerate(existing_rows, start=1):
                if len(row) > 0 and row[0] == user_name:
                    user_row = index
                    break

            if user_row is None:
                user_row = len(existing_rows) + 1
                sheet.update_cell(user_row, 1, user_name)

            # Cards go in the following columns
            cards = new_cards.split("-")
            for col, card in enumerate(cards, start=2):
                sheet.update_cell(user_row, col, card)

            await ctx.send("Tus cards han sido actualizadas correctamente en la hoja de cálculo.") # Confirmation message in Spanish, will be used multiple times

        except Exception as e:
            await ctx.send(f"Ha ocurrido un error: {e}") # Exception message in Spanish


    @commands.command()
    async def buscocartas(self, ctx, *, new_cards: str): # Replaces existing text in cells
        try:
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("TCG_Busco")

            existing_rows = sheet.get_all_values()
            user_row = None

            for index, row in enumerate(existing_rows, start=1): 
                if len(row) > 0 and row[0] == user_name:
                    user_row = index
                    break

            if user_row is None:
                user_row = len(existing_rows) + 1
                sheet.update_cell(user_row, 1, user_name)

            cards = new_cards.split("-")
            for col, card in enumerate(cards, start=2):
                sheet.update_cell(user_row, col, card)

            await ctx.send("Tus cartas han sido actualizadas correctamente en la hoja de cálculo.")

        except Exception as e:
            await ctx.send(f"Ha ocurrido un error: {e}")

    @commands.command()
    async def buscarcard(self, ctx, *, card: str):
        """
        Looks for a card and sends all the users who have it.
        """
        try:
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("TCG_Tengo")

            existing_rows = sheet.get_all_values()
            users_with_card = []

            for row in existing_rows:
                if any(card.lower() in cell.lower() for cell in row if cell):
                    users_with_card.append(row[0])

            if users_with_card:
                users = "\n".join(users_with_card)
                await ctx.send(f"Usuarios con la carta '{card}':\n{users}")
            else:
                await ctx.send(f"No se han encontrado usuarios con la carta '{card}'.")

        except Exception as e:
            await ctx.send(f"Ha ocurrido un error: {e}")

    @commands.command()
    async def tengocartasañadir(self, ctx, *, new_cards: str): # Adds text to the existing one
        try:
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("TCG_Tengo")

            existing_rows = sheet.get_all_values()
            user_row = None

            for index, row in enumerate(existing_rows, start=1):
                if len(row) > 0 and row[0] == user_name:
                    user_row = index
                    break

            if user_row is None:
                user_row = len(existing_rows) + 1
                sheet.update_cell(user_row, 1, user_name)  

            cards = new_cards.split("-")
            for col, card in enumerate(cards, start=2):
                current_content = sheet.cell(user_row, col).value

                if current_content is None:
                    current_content = ""
                new_content = f"{current_content}, {card}".strip()

                sheet.update_cell(user_row, col, new_content)

            await ctx.send("Tus cartas han sido actualizadas correctamente en la hoja de cálculo.")

        except Exception as e:
            await ctx.send(f"Ha ocurrido un error: {e}")


    @commands.command()
    async def buscocartasañadir(self, ctx, *, new_cards: str): # Adds text to the existing one

        try:
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("TCG_Busco")

            existing_rows = sheet.get_all_values()
            user_row = None

            for index, row in enumerate(existing_rows, start=1): 
                if len(row) > 0 and row[0] == user_name:
                    user_row = index
                    break

            if user_row is None:
                user_row = len(existing_rows) + 1
                sheet.update_cell(user_row, 1, user_name)

            cards = new_cards.split("-")
            for col, card in enumerate(cards, start=2):
                current_content = sheet.cell(user_row, col).value

                if current_content is None:
                    current_content = ""

                new_content = f"{current_content}, {card}".strip() 

                sheet.update_cell(user_row, col, new_content)
            await ctx.send("Tus cartas han sido actualizadas correctamente en la hoja de cálculo.")

        except Exception as e:
            await ctx.send(f"Ha ocurrido un error: {e}")

async def setup(bot):
    from databases.SheetConnection import connectSheet
    await bot.add_cog(cardsCog(bot, connectSheet))
