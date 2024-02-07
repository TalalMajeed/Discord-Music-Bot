from server import render
from discord.ext.commands import Bot
from discord.utils import get
from discord import FFmpegPCMAudio, Intents
from yt_dlp import YoutubeDL
import yt_dlp.utils
import requests
import re
import nacl
import os
import asyncio

#GLOBAL DECLARATIONS

intents = Intents.all()
intents.members = True

bot = Bot("-", intents=intents)
songs = []
version = "Release 2.0.3"
current = ""
loop = -1
loopdata = []

#VIDEO CONTROLS

#FUNCTIONS


def polish(text):
  print(text)
  if not "youtube.com/watch?v=" in text:
    s = requests.utils.quote(text)
    x = requests.get(
        "https://www.youtube.com/results?search_query=" + s,
        headers={
            'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        })
    print(x)
    u = re.search(r"watch\?v=(\S{11})", x.text)
    return "https://www.youtube.com/watch?v=" + u.groups()[0]
  else:
    return text


def order(ctx):
  global songs
  global loopdata
  global loop
  if len(songs) > 0:
    new = songs[0]
    songs.pop(0)
    asyncio.run_coroutine_threadsafe(p(ctx, new), bot.loop)
  else:
    if len(loopdata) > 0 and loop == 1:
      for i in loopdata:
        songs.append(i)
      order(ctx)


#EVENT HANDLERS


@bot.event
async def on_ready():
  print("Music Bot Started.........")


#JOIN COMMAND


@bot.command()
async def j(ctx):
  vc = ctx.author.voice
  if not vc is None:
    try:
      await ctx.channel.send("Joining Channel...")
      await vc.channel.connect()
    except:
      await ctx.channel.send("Something Went Wrong :\\")
    return True
  else:
    await ctx.channel.send("Please Connect to a Voice Channel...")
    return False


#LEAVE COMMAND


@bot.command()
async def l(ctx):
  global songs
  global loop
  global loopdata
  vc = get(bot.voice_clients, guild=ctx.guild)
  if not vc is None:
    songs = []
    loopdata = []
    loop = -1
    await vc.disconnect()
    await ctx.channel.send("See you Soon!!")


#SKIP COMMAND


@bot.command()
async def s(ctx):
  global songs
  global loopdata
  vc = get(bot.voice_clients, guild=ctx.guild)
  if not vc is None:
    try:
      await vc.stop()
    except:
      pass
    if len(songs) > 0:
      await ctx.channel.send("Playing Next Song...")
    elif len(loopdata) > 0:
      await ctx.channel.send("Playing Next Song...")
    else:
      await ctx.channel.send("No More Songs to Play...")


#PLAY COMMAND


@bot.command()
async def p(ctx, *song):
  global songs
  global current
  global loop
  global loopdata
  yt_dlp.utils.std_headers[
      'User-agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
  vc = get(bot.voice_clients, guild=ctx.guild)
  test = False
  YDL_OPTIONS = {
      'format': 'bestaudio',
      'noplaylist': 'True',
      'cachedir': 'False',
      'cookiefile': 'cookies.txt'
  }
  FFMPEG_OPTIONS = {
      'before_options':
      '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
      'options': '-vn'
  }

  if vc is None:
    test = await j(ctx)
  else:
    if not vc.is_connected():
      test = await j(ctx)
    else:
      test = True

  vc = get(bot.voice_clients, guild=ctx.guild)

  if test == True:
    if len(" ".join(song)) > 0:
      url = polish(" ".join(song))
      #MAIN RENDERING
      if not vc.is_playing():
        await ctx.channel.send("Now Playing: " + url)
        current = url
        #VIDEO OPTIONS
        with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
        URL = info['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: order(ctx))
        vc.is_playing()
      else:
        songs.append(url)
        if loop == 1:
          loopdata.append(url)
        await ctx.channel.send("Song has been Queued!!")
    else:
      await ctx.channel.send("Please enter Valid Text or Link")


#FORCE COMMAND


@bot.command()
async def f(ctx, *song):
  global songs
  global loop
  global loopdata
  url = " ".join(song)
  vc = get(bot.voice_clients, guild=ctx.guild)
  if not vc is None:
    songs = []
    if loop == 1:
      loopdata = []
      loop = -1
      await ctx.channel.send("Looping Disabled...")
    try:
      await vc.stop()
    except:
      pass
    await p(ctx, url)


#PAUSE COMMAND
@bot.command()
async def k(ctx):
  vc = get(bot.voice_clients, guild=ctx.guild)
  if not vc is None:
    if vc.is_playing():
      vc.pause()
      await ctx.channel.send("Paused Player...")


#CONTINUE COMMAND
@bot.command()
async def c(ctx):
  vc = get(bot.voice_clients, guild=ctx.guild)
  if not vc is None:
    if vc.is_paused():
      vc.resume()
      await ctx.channel.send("Started Player...")


#LOOP COMMAND
@bot.command()
async def i(ctx):
  global loop
  global loopdata
  global songs
  global current
  vc = get(bot.voice_clients, guild=ctx.guild)
  if not vc is None:
    loop *= -1
    if loop == 1:
      loopdata.append(current)
      for i in songs:
        loopdata.append(i)
      await ctx.channel.send("Looping Enabled...")
    elif loop == -1:
      loopdata = []
      await ctx.channel.send("Looping Disabled...")


#HELP COMMAND


@bot.command()
async def h(ctx):
  await ctx.channel.send(
      "WELCOME TO DISCORD MUSIC BOT 2.0\n---------------------\nDEVELOPER:\nM.Talal Majeed\n--------------------\nVERSION:\n"
      + version +
      "\n--------------------\nCOMMANDS:\n-p SONG : Play a Song\n-f SONG : Force Change a Song\n-j : Join a Voice Channel\n-l : Leave a Voice Channel\n-k : Pause the Player\n-c : Resume the Player\n-h : Get Help\n-i : Enable / Disable Looping\n--------------------"
  )


#RENDER

render()
bot.run(os.environ['TOKEN'])
