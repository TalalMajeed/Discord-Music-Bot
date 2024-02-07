import discord
from discord.ext import commands
from main import render


print('Bot starting...')

intents = discord.Intents.default()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')
    
render()
bot.run("ODk2MzM4MDQxODE0MjU3NzE0.GjOSi2.gdcPXklF1aoxdrzhuSHBIQ9jYNBTprc0tlfElM")