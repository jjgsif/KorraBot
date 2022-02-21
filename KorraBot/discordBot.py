import asyncio
import os

import discord
from youtube_dl import YoutubeDL
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
from discord.ext.commands import Bot
from discord.utils import get

bot: Bot = commands.Bot(command_prefix='$')


@bot.command(name='timer')
async def timer(ctx, seconds):
    number = int(seconds)
    message = await ctx.send("Timer set for: " + str(number))
    while True:
        number -= 1
        await message.edit(content=("Time remaining: " + str(number)))
        await asyncio.sleep(1)


@bot.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a channel, please join one and try again.")


@bot.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I am not in a channel to begin with loser...")

@bot.command(pass_context=True)
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(ctx.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))




@bot.command()
async def pause(ctx):
    voice = discord.utils.get(ctx.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(ctx.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command(name='end')
async def end(ctx):
    await exit()


print("Bot has join chat")
bot.run("OTQwODUxNzI3OTg3NTI3NzUx.YgNadA.QhC9C6NS0blHgQ_H2DYRdliSlo4")
