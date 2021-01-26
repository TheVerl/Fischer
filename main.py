#!/usr/bin/env python3

# Import modules
import discord 
from discord.ext import commands
import sys, json, datetime

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
    try:
        data = (lichess.getUser(username))
    except:
        embed = discord.Embed(title="Sorry!", description="Could not find the specified user.")
        await ctx.channel.send(embed=embed)
        return
    print(data)
    print("\n")
    try:
        if (data['closed'] == True):
            embed = discord.Embed(title="Sorry!", description="The specified user's account has been closed.")
            await ctx.channel.send(embed=embed)
            return
    except:
        embed = discord.Embed(title=data["username"] + "'s Lichess account")
        embed.add_field(name="Bullet", value = data["perfs"]["bullet"]["rating"], inline=True)
        embed.add_field(name="Blitz", value = data["perfs"]["blitz"]["rating"], inline=True)
        embed.add_field(name="Rapid", value = data["perfs"]["rapid"]["rating"], inline=True)
        embed.add_field(name="All matches", value = data['count']['all'], inline=True)
        embed.add_field(name="Rated matches", value = data['count']['rated'], inline=True)
        embed.add_field(name="Drawn matches", value=data['count']['draw'], inline=True)
        embed.add_field(name="Wins", value = data['count']['win'], inline=True)
        embed.add_field(name="Losses", value = data['count']['loss'], inline=True)
        embed.add_field(name="W/L Ratio", value = round(data['count']['win'] / data['count']['loss'], 2), inline=True)
        embed.add_field(name="Account creation date", value = data['createdAt'].strftime("%Y-%m-%d %H:%M"), inline=True)
        embed.add_field(name="Last seen", value = data['seenAt'].strftime("%Y-%m-%d %H:%M"), inline=True)
        embed.set_footer(text="Dates and times are in GMT.")
        await ctx.channel.send(embed=embed)

def init():
    with open("discord.token") as f:
        token = f.read()
    f.close()
    bot.run(token)

if __name__ == '__main__':
    init()
