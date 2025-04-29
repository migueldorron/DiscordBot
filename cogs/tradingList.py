from discord.ext import commands
import databases.translations
from gspread.utils import rowcol_to_a1
from collections import defaultdict

class cardsCog(commands.Cog):
    dict=databases.translations.tradingListComandos
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection
        self.cartas_channel_id = [1318194896879882253, 1353112265897017456]

    @commands.command(name="fortrade", aliases=["tengocartas", "ft"], 
                      help="Overwrites the cards you have to trade, using dashes to move to the next rarity. Cards range from 2 Diamonds to 1 Star. Aliases: ft. \n\n Example: -fortrade Wartortle, Charmeleon (GA) - Gardevoir, Greninja, - Pachirisu EX, Charizard EX (SR) - Spiritomb, Pidgeot. \n\n If you want to leave a category blank, just don't type anything and write the next dash.", 
                      brief="Cards")
    async def fortrade(self, ctx, *, new_cards: str): # Replaces existing text in cells
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


    @commands.command(name="lookingfor", aliases=["buscocartas", "lf"], 
                      help="Overwrites the cards you have to trade, using dashes to move to the next rarity. Cards range from 2 Diamonds to 1 Star. Aliases: lf. \n\n Example: -lookingfor Wartortle, Charmeleon (GA) - Gardevoir, Greninja, - Pachirisu EX, Charizard EX (SR) - Spiritomb, Pidgeot. \n\n If you want to leave a category blank, just don't type anything and write the next dash.", 
                      brief="Cards")
    async def lookingfor(self, ctx, *, new_cards: str): # Replaces existing text in cells
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

            sheet_for_trade = connection_excel.worksheet("For_Trade")
            result = self.find_trades_for_user(user_name, sheet, sheet_for_trade)
            await ctx.send(result)

        except Exception as e:
            await ctx.send(f"Error: {e}")


    @commands.command(name="search", aliases=["buscarcarta"], 
                    help="Looks for a card and sends everyone who has or is looking for it. \n\n Example: -search Dragonite",
                    brief="Cards")
    async def search(self, ctx, *, card: str):
        try:
            if not await self.channel_check(ctx):
                return 
            connection_excel = self.connection()
            await self.search_in_worksheet(ctx, card, connection_excel, "For_Trade")
            await ctx.send("----")
            await self.search_in_worksheet(ctx, card, connection_excel, "Looking_For")

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="fortradeadd", aliases=["tengocartasañadir", "fta"], 
                      help="Overwrites the cards you have to trade, using dashes to move to the next rarity. Cards range from 2 Diamonds to 1 Star. Aliases: fta. \n\n Example: -fortradeadd Wartortle, Charmeleon (GA) - Gardevoir, Greninja, - Pachirisu EX, Charizard EX (SR) - Spiritomb, Pidgeot. \n\n If you want to leave a category blank, just don't type anything and write the next dash.", 
                      brief="Cards")
    async def fortradeadd(self, ctx, *, new_cards: str): # Adds text to the existing one
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

    @commands.command(name="lookingforadd", aliases=["buscocartasañadir", "lfa"], 
                      help="Overwrites the cards you have to trade, using dashes to move to the next rarity. Cards range from 2 Diamonds to 1 Star. Aliases: lfa. \n\n Example: -lookingforadd Wartortle, Charmeleon (GA) - Gardevoir, Greninja, - Pachirisu EX, Charizard EX (SR) - Spiritomb, Pidgeot. \n\n If you want to leave a category blank, just don't type anything and write the next dash.", 
                      brief="Cards")    
    async def lookingforadd(self, ctx, *, new_cards: str):
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

            sheet_for_trade = connection_excel.worksheet("For_Trade")
            result = self.find_trades_for_user(user_name, sheet, sheet_for_trade)
            await ctx.send(result)
            
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="searchuser", aliases=["buscarusuario"], 
                      help="Returns what a user has to offer. You can specify rarity ranging from 3 to 5 (3 diamonds, EX, Full Art).\n\n Example: -searchuser dorron, 4", 
                      brief="Cards")
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




    @commands.command(name="findtrades", aliases=["encontrartrades"],
                    help="Sends you all the cards you're looking for that someone else is willing to trade.",
                    brief="Cards")
    async def findtrades(self, ctx):
        connection = self.connection()
        sheet_looking = connection.worksheet("Looking_For")
        sheet_trade = connection.worksheet("For_Trade")

        result = self.find_trades_for_user(ctx.author.name, sheet_looking, sheet_trade)
        await ctx.send(result)



    async def channel_check(self, ctx):
        if ctx.channel.id not in self.cartas_channel_id:
            await ctx.send("Not the correct channel, go to the correct channel in your server.")
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

    async def find_trades_for_user(self, user_name, sheet_looking, sheet_trade):
        dataLookingFor = sheet_looking.get_all_values()
        rowUser = None

        for row in dataLookingFor[1:]:
            if row and row[0].strip().lower() == user_name.strip().lower():
                rowUser = row
                break

        if not rowUser:
            return "You don't have cards you're looking for."

        desired_cards = set()
        for i in [3, 4]:
            if i < len(rowUser) and rowUser[i]:
                cards = [card.strip().lower() for card in rowUser[i].split(",") if card.strip()]
                desired_cards.update(cards)

        if not desired_cards:
            return "You haven’t listed any cards in columns D and E."

        dataForTrade = sheet_trade.get_all_values()
        card_to_traders = {}

        for row in dataForTrade[1:]:
            if not row or row[0].strip().lower() == user_name.strip().lower():
                continue

            trader = row[0]
            for i in [3, 4]:
                if i < len(row) and row[i]:
                    trader_cards = [card.strip().lower() for card in row[i].split(",") if card.strip()]
                    for card in trader_cards:
                        if card in desired_cards:
                            if card not in card_to_traders:
                                card_to_traders[card] = [trader]
                            elif trader not in card_to_traders[card]:
                                card_to_traders[card].append(trader)

        if card_to_traders:
            result = "\n".join(
                f"{card.title()} — {', '.join(card_to_traders[card])}" for card in card_to_traders
            )
            return f"📦 Users offering what you're looking for:\n{result}"
        else:
            return "No one is currently offering the cards you listed."


async def setup(bot):
    from databases.SheetConnection import connectSheet
    await bot.add_cog(cardsCog(bot, connectSheet))