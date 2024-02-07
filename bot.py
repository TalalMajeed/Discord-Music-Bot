import _thread
import discord
from discord.ext import commands

print('Bot starting...')

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')

def run_flask():
    # Assuming main.py contains the Flask app
    from main import app
    app.run(debug=True, port=80)

_thread.start_new_thread(run_flask, ())

bot.run("ODk2MzM4MDQxODE0MjU3NzE0.GjOSi2.gdcPXklF1aoxdrzhuSHBIQ9jYNBTprc0tlfElM")