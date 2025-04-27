from discord.ext import commands
import databases.translations
from gspread.utils import rowcol_to_a1

class cardsCog(commands.Cog):
    dict=databases.translations.tradingListComandos
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection
        self.cartas_channel_id = [1318194896879882253, 1353112265897017456]

    @commands.command(name="fortrade", aliases=["tengocartas", "ft"], help="Overwrites the cards you have to trade.", brief="Cards")
    async def tengocartas(self, ctx, *, new_cards: str): # Replaces existing text in cells
        try:
            if not await self.channel_check(ctx):
                return
            user_name = ctx.author.name
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")
            existing_rows = sheet.get_all_values()
            user_row = self.find_user(user_name,existing_rows)
            user_row = self.user_already_exists(user_name, sheet, existing_rows, user_row)
            self.write_cards(new_cards, sheet, user_row)
            await ctx.send(self.dict[ctx.invoked_with][0]) # Confirmation message

        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.command(name="lookingfor", aliases=["buscocartas", "lf"], help="Overwrites the cards you are looking for.", brief="Cards")
    async def buscocartas(self, ctx, *, new_cards: str): # Replaces existing text in cells
        try:
            if not await self.channel_check(ctx):
                return
            user_name = ctx.author.name
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("Looking_For")
            existing_rows = sheet.get_all_values()
            user_row = self.find_user(user_name, sheet)
            user_row = self.user_already_exists(user_name, sheet, existing_rows, user_row)

            self.write_cards(new_cards, sheet, user_row)

            await ctx.send(self.dict[ctx.invoked_with][0])

        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.command(name="search", aliases=["buscarcarta"], help="Looks for a card and sends everyone who has or is looking for it.", brief="Cards")
    async def buscarcarta(self, ctx, *, card: str):
        try:
            if not await self.channel_check(ctx):
                return 
            connection_excel = self.connection()
            await self.search_in_worksheet(ctx, card, connection_excel, "For_Trade")
            await ctx.send("----")
            await self.search_in_worksheet(ctx, card, connection_excel, "Looking_For")

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="fortradeadd", aliases=["tengocartasañadir", "fta"], help="Adds the cards you have to trade to the existing ones.", brief="Cards")
    async def tengocartasañadir(self, ctx, *, new_cards: str): # Adds text to the existing one
        try:
            if not await self.channel_check(ctx):
                return
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")
            existing_rows = sheet.get_all_values()            
            user_row = self.find_user(user_name, sheet)
            user_row = self.user_already_exists(user_name, sheet, existing_rows, user_row)  
            self.add_new_cards(new_cards, sheet, user_row)
            await ctx.send(self.dict[ctx.invoked_with][0])

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="lookingforadd", aliases=["buscocartasañadir", "lfa"], help="Adds the cards you are looking for to the existing ones.", brief="Cards")
    async def buscocartasañadir(self, ctx, *, new_cards: str):
        try:
            if not await self.channel_check(ctx):
                return
            user_name = ctx.author.name

            connection_excel = self.connection()
            sheet = connection_excel.worksheet("Looking_For")
            existing_rows = sheet.get_all_values()            
            user_row = self.find_user(user_name, sheet)
            user_row = self.user_already_exists(user_name, sheet, existing_rows, user_row)
            self.add_new_cards(new_cards, sheet, user_row)
            await ctx.send(self.dict[ctx.invoked_with][0])
            
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="searchuser", aliases=["buscarusuario"], help="Returns what a user has to offer. You can specify rarity ranging from 3 to 5 (3 diamonds, EX, Full Art).", brief="Cards")
    async def buscarusuario(self, ctx, *, args: str):
        try:
            if not await self.channel_check(ctx):
                return
            split_args = [x.strip() for x in args.split(',')]
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("For_Trade")
            data = sheet.get_all_values()
            user_found = False
            if len(split_args) == 2:
                user, rarity = split_args[0].lower(), split_args[1]
                rarity = int(rarity)
                for row in data[1:]:
                    if len(row) > 0 and row[0].lower() == user:
                        header = data[0][rarity-1] if (rarity-1) < len(data[0]) else "Unknown"
                        value = row[rarity-1] if (rarity-1) < len(row) else "Wrong rarity."
                        await ctx.send(f"{header}: {value}")
                        user_found=True
                        break
            elif len(split_args) == 1:
                user = split_args[0].lower()
                for row in data[1:]:
                    if len(row) > 0 and row[0].lower() == user:
                            user_found=True                        
                            for index in range(2, 5):
                                await ctx.send(f"{data[0][index]}: {row[index]}")
                            break
            if not user_found:
                await ctx.send(self.dict[ctx.invoked_with][0])

        except ValueError:
            await ctx.send(self.dict[ctx.invoked_with][1])
            return
        except Exception as e:
            await ctx.send(f"Error: {e}")




    async def channel_check(self, ctx):
        if ctx.channel.id not in self.cartas_channel_id:
            await ctx.send("Not the correct channel, go to the respective channel, probably <#1353112265897017456>.")
            return False
        return True

    def add_new_cards(self, new_cards, sheet, user_row):
        cards = new_cards.split("-")
        row_values = sheet.row_values(user_row)
        updates = []
        for col, card in enumerate(cards, start=2):
            current_content = row_values[col-1] if (col-1)<len(row_values) else ""
            new_content = f"{current_content}, {card}".strip()
            updates.append({'range': rowcol_to_a1(user_row, col),'values': [[new_content]]})
        sheet.batch_update(updates)

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
        updates = []
        for col, card in enumerate(cards, start=2):
            updates.append({'range': rowcol_to_a1(user_row, col),'values': [[card]]})
        sheet.batch_update(updates)

    def user_already_exists(self, user_name, sheet, existing_rows, user_row):
        if user_row is None:
            for index, row in enumerate(existing_rows[1:], start=2):
                if len(row) == 0 or not row[0].strip():
                    user_row = index
                    break
            else:
                user_row = len(existing_rows) + 1

            sheet.update_cell(user_row, 1, user_name)
        return user_row
    
    def find_user(self, user_name, existing_rows):
        user_row = None
        for index, row in enumerate(existing_rows, start=1): 
            if len(row) > 0 and row[0] == user_name:
                user_row = index
                break
        return user_row

    async def search_in_worksheet(self, ctx, card, connection_excel, worksheet_name):
        sheet = connection_excel.worksheet(worksheet_name)
            
        existing_rows = sheet.get_all_values()
        users_with_card = []

        self.find_cards(card, existing_rows, users_with_card)

        await self.send_found_cards(ctx, card, sheet, users_with_card)


async def setup(bot):
    from databases.SheetConnection import connectSheet
    await bot.add_cog(cardsCog(bot, connectSheet))
