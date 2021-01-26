#!/usr/bin/env python3

# Import modules
import discord 
from discord.ext import commands
import sys, json, datetime
from datetime import datetime

# Import scripts
sys.path.insert(0, 'chess/')
import chesscom
import lichess


client = discord.Client()
bot = commands.Bot(command_prefix="$")
token = ""

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="against Spassky"))
    with open ("discord.token") as f:
        token = f.read()
    f.close()
    print("We have logged in as {0.user}".format(bot))
    lichess.setup()
    chesscom.setup()

@bot.command(name="cmds")
async def help(ctx):
    embed = discord.Embed(title="Command List")
    embed.add_field(name="$ping", value = "pong!", inline=False)
    embed.add_field(name="$lichessuser", value = "Get the info and stats of a specific user on lichess.org", inline=False)
    embed.add_field(name="$chesscomuser", value = "Get the info and stats of a specific user on chess.com", inline=False)
    embed.add_field(name="$help", value = "What you see before you now.", inline=False)
    embed.set_footer(text="Developed by Verl.")
    await ctx.channel.send(embed=embed)
    return



@bot.command(name="ping")
async def testCommand(ctx):
    print({ctx.author.name + "#" + ctx.author.discriminator}, " sent ", {ctx.message.content})
    await ctx.channel.send("pong")
    print("Command executed succesfully.")

@bot.command(name="chesscomuser")
async def getChesscomUser(ctx, username):
    print({ctx.author.name + "#" + ctx.author.discriminator}, " sent ", {ctx.message.content})
    if username == None:
        embed = discord.Embed(title="Sorry!", description="Was not given a user to search for.")
        await ctx.channel.send(embed=embed)
        print("Command executed unsuccesfully.")
    try:
        info = chesscom.getUserInfo(username).json
        stat = chesscom.getUserStat(username).json
        matches = chesscom.getUserMatches(username, stat)
        creation = datetime.fromtimestamp(info["joined"])
        last = datetime.fromtimestamp(info["last_online"])
        embed = discord.Embed(title=username + "'s Chess.com account")
        if (chesscom.getUserStatus):
             embed.set_author(name="Online", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Green_sphere.svg/1024px-Green_sphere.svg.png")
        else:
            embed.set_author(name="Offline")
        embed.add_field(name="Bullet", value  = stat["chess_bullet"]["last"]["rating"])
        embed.add_field(name="Blitz", value = stat["chess_blitz"]["last"]["rating"])
        embed.add_field(name="Rapid", value = stat["chess_rapid"]["last"]["rating"])
        embed.add_field(name="Total matches played", value = matches["total"])
        embed.add_field(name="Total W/L Ratio", value = round(matches["sum"]["win"] / matches["sum"]["loss"], 2), inline=False)
        embed.add_field(name="Matches won", value = matches["sum"]["win"])
        embed.add_field(name="Matches lost", value = matches["sum"]["loss"])
        embed.add_field(name="Matches drawn", value = matches["sum"]["draw"])
        embed.add_field(name="Rapids won", value = matches["win"]["rapid"])
        embed.add_field(name="Rapids lost", value = matches["loss"]["rapid"])
        embed.add_field(name="Rapids drawn", value = matches["draw"]["rapid"])
        embed.add_field(name="Blitzes won", value = matches["win"]["blitz"])
        embed.add_field(name="Blitzes lost", value = matches["loss"]["blitz"])
        embed.add_field(name="Blitzes drawn", value = matches["draw"]["blitz"])
        embed.add_field(name="Bullets won", value = matches["win"]["bullet"])
        embed.add_field(name="Bullets lost", value = matches["loss"]["bullet"])
        embed.add_field(name="Bullets drawn", value = matches["draw"]["bullet"])
        embed.add_field(name="Rapid W/L Ratio", value = round(matches["win"]["rapid"] / matches["loss"]["rapid"], 2))
        embed.add_field(name="Blitz W/L Ratio", value = round(matches["win"]["blitz"] / matches["loss"]["blitz"], 2))
        embed.add_field(name="Bullet W/L Ratio", value = round(matches["win"]["bullet"] / matches["loss"]["bullet"], 2))
        embed.add_field(name="Account creation date", value = creation.strftime("%Y-%m-%d %H:%M"))
        embed.add_field(name="Last seen", value = last.strftime("%Y-%m-%d %H:%M"), inline=True)
        embed.set_footer(text="Dates and times are in GMT. Developed by Verl.")
        await ctx.channel.send(embed=embed)
        print("Command executed succesfully.")
    except:
        embed = discord.Embed(title="Sorry!", description="Could not find the specified user.")
        await ctx.channel.send(embed=embed)
        print("Command executed unsuccesfully.")
    return

@bot.command(name="lichessuser")
async def getLichessUser(ctx, username):
    print({ctx.author.name + "#" + ctx.author.discriminator}, " sent ", {ctx.message.content})
    if username == None:
        embed = discord.Embed(title="Sorry!", description="Was not given a user to search for.")
        await ctx.channel.send(embed=embed)
        print("Command executed unsuccesfully.")
    try:
        data = (lichess.getUser(username))
    except:
        embed = discord.Embed(title="Sorry!", description="Could not find the specified user.")
        await ctx.channel.send(embed=embed)
        print("Command executed unsuccesfully.")
        return
    try:
        if (data['closed'] == True):
            embed = discord.Embed(title="Sorry!", description="The specified user's account has been closed.")
            await ctx.channel.send(embed=embed)
            print("Command executed unsuccesfully.")
            return
    except:
        embed = discord.Embed(title=data["username"] + "'s Lichess account")
        if (data['online'] == True):
            embed.set_author(name="Online", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Green_sphere.svg/1024px-Green_sphere.svg.png")
        else:
            embed.set_author(name="Offline")
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
        embed.set_footer(text="Dates and times are in GMT. Developed by Verl.")
        await ctx.channel.send(embed=embed)
        print("Command executed succesfully.")

def init():
    with open("discord.token") as f:
        token = f.read()
    f.close()
    bot.run(token)

if __name__ == '__main__':
    init()
