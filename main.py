#!/usr/bin/env python3

# Import modules
import discord 
from discord.ext import commands
import sys

# Import scripts
sys.path.insert(0, 'chess/')
import chesscom
import lichess


client = discord.Client()
bot = commands.Bot(command_prefix="$")
token = ""

@bot.event
async def on_ready():
    with open ("discord.token") as f:
        token = f.read()
    f.close()
    print("We have logged in as {0.user}".format(bot))
    lichess.setup()
    print("Lichess module is initialised.")

@bot.command(name="ping")
async def testCommand(ctx):
    await ctx.channel.send("pong")

@bot.command(name="lichessuser")
async def getLichessUser(ctx, username):
    embed = discord.Embed(title="JohnSmith#0000\nRating: 9999\nRank: #1")
    await ctx.send(embed=embed)
    #await ctx.channel.send(lichess.getUser(username))

def init():
    with open("discord.token") as f:
        token = f.read()
    f.close()
    bot.run(token)

if __name__ == '__main__':
    init()
