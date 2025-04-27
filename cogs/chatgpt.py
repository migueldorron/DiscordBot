import discord
import openai
from discord.ext import commands
from dotenv import load_dotenv
import os


load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")
client = openai.OpenAI(api_key=openai.api_key)

class ChatGPTCog(commands.Cog):
    def __init__(self, bot, connectionBBDD):
        self.bot = bot
        self.connectionBBDD = connectionBBDD 

    # Command to ask ChatGPT
    @commands.command(name="chatgpt", help="Sends ChatGPT a prompt.", brief="Other")
    async def chatgpt(self, ctx, *, question: str):        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}]
            )
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": question}]
            )
            answer = response.choices[0].message.content

            await ctx.send(answer)

        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    connectionBBDD = bot.connectionBBDD
    await bot.add_cog(ChatGPTCog(bot, connectionBBDD))