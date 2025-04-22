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
            await self.channel_check(ctx)            
            user_name = ctx.author.name
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")

            existing_rows, user_row = self.find_user(user_name, sheet)
            user_row = self.user_already_exists(user_name, sheet, existing_rows, user_row)
            self.write_cards(new_cards, sheet, user_row)
            await ctx.send(self.dict[ctx.invoked_with][0]) # Confirmation message

        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.command(name="buscocartas", aliases=["lookingfor", "lf"])
    async def buscocartas(self, ctx, *, new_cards: str): # Replaces existing text in cells
        try:
            await self.channel_check(ctx) 
            user_name = ctx.author.name
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("Looking_For")

            existing_rows, user_row = self.find_user(user_name, sheet)

            user_row = self.user_already_exists(user_name, sheet, existing_rows, user_row)

            self.write_cards(new_cards, sheet, user_row)

            await ctx.send(self.dict[ctx.invoked_with][0])

        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.command(name="buscarcarta", aliases=["search"])
    async def buscarcarta(self, ctx, *, card: str):
        """
        Looks for a card and sends all the users who have it.
        """
        try:
            await self.channel_check(ctx)   
            connection_excel = self.connection()
            await self.search_in_worksheet(ctx, card, connection_excel, "For_Trade")
            await ctx.send("----")
            await self.search_in_worksheet(ctx, card, connection_excel, "Looking_For")

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="tengocartasañadir", aliases=["fortradeadd", "fta"])
    async def tengocartasañadir(self, ctx, *, new_cards: str): # Adds text to the existing one
        try:
            await self.channel_check(ctx)
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")
            existing_rows, user_row = self.find_user(user_name, sheet)
            user_row = self.user_already_exists(user_name, sheet, existing_rows, user_row)  
            self.add_new_cards(self, new_cards, sheet, user_row)
            await ctx.send(self.dict[ctx.invoked_with][0])

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="buscocartasañadir", aliases=["lookingforadd", "lfa"])
    async def buscocartasañadir(self, ctx, *, new_cards: str): # Adds text to the existing one
        try:
            await self.channel_check(ctx)
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("Looking_For")
            existing_rows, user_row = self.find_user(user_name, sheet)
            user_row = self.user_already_exists(user_name, sheet, existing_rows, user_row)
            self.add_new_cards(self, new_cards, sheet, user_row)

            await ctx.send(self.dict[ctx.invoked_with][0])
            
        except Exception as e:
            await ctx.send(f"Error: {e}")



    @commands.command(name="buscarusuario", aliases=["searchuser"])
    async def buscarusuario(self, ctx, *, args: str):
        try:
            await self.channel_check(ctx)
            user, rarity = [x.strip() for x in args.split(',')]
            rarity = int(rarity)
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")

            for row in range(2,sheet.row_count+1):
                if sheet.cell(row,1).value==user:
                    await ctx.send(f"{sheet.cell(1,rarity).value}: {sheet.cell(row,rarity).value}")
                    break

        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.command(name="buscarusuario", aliases=["searchuser"])
    async def buscarusuario(self, ctx, *, user: str):
        try:
            await self.channel_check(ctx)
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")

            for row in range(2,sheet.row_count+1):
                if sheet.cell(row,1).value==user:
                    for rarity in range(3,6):
                        await ctx.send(f"{sheet.cell(1,rarity).value}: {sheet.cell(row,rarity).value}")
                    break

        except Exception as e:
            await ctx.send(f"Error: {e}")

    async def channel_check(self, ctx):
        if ctx.channel.id not in self.cartas_channel_id:
            await ctx.send("Not the correct channel, go to the respective channel, probably <#1353112265897017456>.")
            return

    def add_new_cards(self, new_cards, sheet, user_row):
        cards = new_cards.split("-")
        for col, card in enumerate(cards, start=2):
                current_content = sheet.cell(user_row, col).value
                if current_content is None:
                    current_content = ""
                new_content = f"{current_content}, {card}".strip()
                sheet.update_cell(user_row, col, new_content)

    async def send_found_cards(self, ctx, card, sheet, users_with_card):
        if users_with_card:
            users = "\n".join(users_with_card)
            await ctx.send(f"{sheet.title}\n{users}")
        else:
            await ctx.send(self.dict[ctx.invoked_with][0].format(card=card, sheet=sheet.title))



    def find_cards(self, card, existing_rows, users_with_card):
        for row in existing_rows:
            for column_rarity, cell in enumerate(row):
                if cell:
                    cards_in_cell = [c.strip() for c in cell.split(',')]
                    for c in cards_in_cell:
                        if card.lower() in c.lower():
                            column_header = existing_rows[0][column_rarity]
                            users_with_card.append(f"{row[0]} - {c} ({column_header})")
                            break

    def write_cards(self, new_cards, sheet, user_row):
        cards = new_cards.split("-")
        for col, card in enumerate(cards, start=2):
            sheet.update_cell(user_row, col, card)

    def user_already_exists(self, user_name, sheet, existing_rows, user_row):
        if user_row is None:
            user_row = len(existing_rows) + 1
            sheet.update_cell(user_row, 1, user_name)
        return user_row
    
    def find_user(self, user_name, sheet):
        existing_rows = sheet.get_all_values()
        user_row = None
        for index, row in enumerate(existing_rows, start=1): 
            if len(row) > 0 and row[0] == user_name:
                user_row = index
                break
        return existing_rows,user_row

    async def search_in_worksheet(self, ctx, card, connection_excel, worksheet_name):
        sheet = connection_excel.worksheet(worksheet_name)
            
        existing_rows = sheet.get_all_values()
        users_with_card = []

        self.find_cards(card, existing_rows, users_with_card)

        await self.send_found_cards(ctx, card, sheet, users_with_card)


async def setup(bot):
    from databases.SheetConnection import connectSheet
    await bot.add_cog(cardsCog(bot, connectSheet))
