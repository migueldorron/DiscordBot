from discord.ext import commands
import databases.translations

class usersCog(commands.Cog):
    dict=databases.translations.usersComandos
    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection
        self.cartas_channel_id = [1318194896879882253, 1353112265897017456]

    @commands.command(name="friendcode", help="Returns someone's friend code.", brief="Users")
    async def friendcode(self, ctx, user :str):
        try:
            if ctx.channel.id not in self.cartas_channel_id:
                await ctx.send("Not the channel, go to <#1353112265897017456>.")
                return
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("Friend_Codes")

            existing_rows = sheet.get_all_values()
            user_row = None

            for index, row in enumerate(existing_rows, start=1):
                if len(row) > 0 and row[0] == user:
                    user_row = index
                    break

            if user_row is None:
                await ctx.send("Not found :x:")
                return
            
            code=None

            for row in existing_rows:
                if any(user.lower() in cell.lower() for cell in row if cell):
                    code=(row[1])
                    break

            await ctx.send(code)
            
        except Exception as e:
            await ctx.send(f"Error: {e}")

    
    @commands.command(name="addid", aliases=["añadirid"], help="Adds your ID to the sheet.", brief="Users")
    async def añadirid(self,ctx,id):
        try:
            if ctx.channel.id not in self.cartas_channel_id:
                await ctx.send("Not the channel, go to <#1353112265897017456>.")
                return
            user=ctx.author.name
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("Friend_Codes")

            existing_rows = sheet.get_all_values()
            user_row = None

            for index, row in enumerate(existing_rows, start=1):
                if len(row) > 0 and row[0] == user:
                    await ctx.send(self.dict[ctx.invoked_with][0])
                    return
            
            user_row = len(existing_rows) + 1
            sheet.update_cell(user_row, 1, user)
            sheet.update_cell(user_row, 2, id)

            await ctx.send(self.dict[ctx.invoked_with][1])
            
        except Exception as e:
            await ctx.send(f"Ha ocurrido un error: {e}")


    @commands.command(name="editid", aliases=["editarid"], help="Edits your current ID in the sheet.", brief="Cards")
    async def editarid(self, ctx, user :str):
        try:
            if ctx.channel.id not in self.cartas_channel_id:
                await ctx.send("Not the channel, go to <#1353112265897017456>.")
                return            
            connection_excel = self.connection()
            sheet = connection_excel.worksheet("Friend_Codes")

            existing_rows = sheet.get_all_values()
            user_row = None

            for index, row in enumerate(existing_rows, start=1):
                if len(row) > 0 and row[0] == user:
                    user_row = index
                    break

            if user_row is None:
                await ctx.send(self.dict[ctx.invoked_with][0])
                return
            
            code=None

            for row in existing_rows:
                if any(user.lower() in cell.lower() for cell in row if cell):
                    code=(row[1])
                    break

            await ctx.send(code)
            
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    from databases.SheetConnection import connectSheet
    await bot.add_cog(usersCog(bot, connectSheet))