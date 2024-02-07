import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')
