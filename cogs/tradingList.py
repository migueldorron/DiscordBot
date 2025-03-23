from discord.ext import commands
import databases.translations

class cardsCog(commands.Cog):
    dict=databases.translations.tradingListComandos
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection
        self.cartas_channel_id = [1318194896879882253, 1353112265897017456]

    @commands.command(name="tengocartas", aliases=["fortrade", "ft"])
    async def tengocartas(self, ctx, *, new_cards: str): # Replaces existing text in cells
        try:
            if ctx.channel.id not in self.cartas_channel_id:
                await ctx.send("Not the channel, go to <#1353112265897017456>.")
                return            
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")

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


            cards = new_cards.split("-")
            for col, card in enumerate(cards, start=2):
                sheet.update_cell(user_row, col, card)

            await ctx.send(self.dict[ctx.invoked_with][0]) # Confirmation message

        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.command(name="buscocartas", aliases=["lookingfor", "lf"])
    async def buscocartas(self, ctx, *, new_cards: str): # Replaces existing text in cells
        try:
            if ctx.channel.id not in self.cartas_channel_id:
                await ctx.send("Not the channel, go to <#1353112265897017456>.")
                return
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("Looking_For")

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

            await ctx.send(self.dict[ctx.invoked_with][0])

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="buscarcarta", aliases=["search"])
    async def buscarcarta(self, ctx, *, card: str):
        """
        Looks for a card and sends all the users who have it.
        """
        try:
            if ctx.channel.id not in self.cartas_channel_id:
                await ctx.send("Not the channel, go to <#1353112265897017456>.")
                return
            
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")

            existing_rows = sheet.get_all_values()
            users_with_card = []

            for row in existing_rows:
                if any(card.lower() in cell.lower() for cell in row if cell):
                    users_with_card.append(row[0])

            if users_with_card:
                users = "\n".join(users_with_card)
                await ctx.send(f"Users:\n{users}")
            else:
                await ctx.send(self.dict[ctx.invoked_with][0].format(card=card))

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="tengocartasañadir", aliases=["fortradeadd", "fta"])
    async def tengocartasañadir(self, ctx, *, new_cards: str): # Adds text to the existing one
        try:
            if ctx.channel.id not in self.cartas_channel_id:
                await ctx.send("Not the channel, go to <#1353112265897017456>.")
                return
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")

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

                await ctx.send(self.dict[ctx.invoked_with][0])

        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.command(name="buscocartasañadir", aliases=["lookingforadd", "lfa"])
    async def buscocartasañadir(self, ctx, *, new_cards: str): # Adds text to the existing one

        try:
            if ctx.channel.id not in self.cartas_channel_id:
                await ctx.send("Not the channel, go to <#1353112265897017456>.")
                return
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("Looking_For")

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
            await ctx.send(self.dict[ctx.invoked_with][0])
            
        except Exception as e:
            await ctx.send(f"Error: {e}")



async def setup(bot):
    from databases.SheetConnection import connectSheet
    await bot.add_cog(cardsCog(bot, connectSheet))
