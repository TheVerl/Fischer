#!/usr/bin/env python3

# Import modules
import discord 
from discord.ext import commands
import sys, json, datetime, csv, random, os, copy
from datetime import datetime

# Import scripts
import puzzle
sys.path.insert(0, 'platforms/')
import chesscom
import lichess
sys.path.insert(0, 'board/')
import board

# Global variables
client = discord.Client()
bot = commands.Bot(command_prefix="$")
prefix = bot.command_prefix
token = ""
legalCommands = ["cmds", "ping", "user", "lichessuser", "chesscomuser", "link", "cmds", "puzzle"]
puzzleFile = open("puzzles.csv", "r")

# Sends messages to host on startup.
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="against Spassky"))
    with open ("discord.token") as f:
        token = f.read()
    f.close()
    print("We have logged in as {0.user}".format(bot))
    lichess.setup()
    chesscom.setup()

# Checks if the message is legal.
@bot.event
async def on_message(message):
    if message.content.startswith(bot.command_prefix):
        ctx = await bot.get_context(message)
        print({ctx.author.name + "#" + ctx.author.discriminator}, " sent ", {ctx.message.content})
        if not ctx.valid:
            embed = discord.Embed(title="Sorry!", description="That is not a legal command.\n Use '.cmds' to find a list of all legal commands.")
            embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
            await ctx.channel.send(embed=embed)
            print("Command executed unsuccesfully.")
        else:
            await bot.process_commands(message)

    return

# Help command.
@bot.command(name="cmds")
async def help(ctx):
    embed = discord.Embed(title="Command List")
    embed.add_field(name=bot.command_prefix + "ping", value = "pong!", inline=False)
    embed.add_field(name=bot.command_prefix + "user", value = "Get info about the chess accounts linked to the mentioned user.\n Usage: " + bot.command_prefix +  "user @[user]")
    embed.add_field(name=bot.command_prefix + "lichessuser", value = "Get info and stats of a specific user on lichess.org.\n Usage: " + bot.command_prefix + "lichessuser [lichess username]", inline=False)
    embed.add_field(name=bot.command_prefix + "chesscomuser", value = "Get info and stats of a specific user on chess.com.\n Usage: " + bot.command_prefix +  "chesscomuser [chess.com username]", inline=False)
    embed.add_field(name=bot.command_prefix + "link", value = "Link your lichess or chess.com account to your Discord account.\n Usage: " + bot.command_prefix +  "link lichess/chesscom [your lichess/chess.com username]")
    embed.add_field(name=bot.command_prefix + "cmds", value = "What you see before you now.", inline=False)
    embed.add_field(name=bot.command_prefix + "puzzle", value = "Play a random puzzle.", inline=False)
    embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
    await ctx.channel.send(embed=embed)
    return

# Pong!
@bot.command(name="ping")
async def testCommand(ctx):
    await ctx.channel.send("pong")
    print("Command executed succesfully.")


# Complete a puzzle.
@bot.command(name="puzzle")
async def pzl(ctx):
    # Get the channel where this command was invoked.
    channel = ctx.channel

    # Get the amount of lines in the file and generate a random number to go to as a row in the file.
    count = sum(1 for row in puzzleFile)
    offset = random.randrange(count)

    # Load the file, find the random row and turn it into a list.
    puzzleFile.seek(offset)
    puzzleFile.readline()
    line = puzzleFile.readline()
    puzzleData = line.split(",")

    # Grab FEN and parse it.
    print("ID:" + str(puzzleData[0]))
    decompiledFEN = puzzle.parseFEN(puzzleData[1].split('/'))

    # Get other info from CSV line.
    rawMoves = puzzleData[2].split(" ")
    moves = []
    for x in range(0, len(rawMoves)):
        duo = []
        for z in range(0, len(rawMoves[x]), 2):
            duo.append(rawMoves[x][z: z + 2])
        moves.append(duo)
    print("valid moves")
    for x in range(len(moves)):
        print(str(moves[x]))
    # Get the rating and determine the difficulty.
    difficulty = ""
    rating = int(puzzleData[3])
    if (rating >= 0 and rating <= 1499):
        difficulty = "Easy"
    elif (rating >= 1500 and rating <= 1999):
        difficulty = "Medium"
    elif (rating >= 2000):
        difficulty = "Hard"

    # Set up the variables needed in the loop.
    completedPuzzle = False
    joe = 0
    FEN = puzzle.updateFEN(moves[0][0], moves[0][1], decompiledFEN)
    FEN = puzzle.clearSquare(moves[0][0], FEN)
    potentialFEN = FEN
    oldFEN = FEN
    lastFEN = FEN
    lastMove = ""
    reply = "INITIAL"
    amountOfMoves = len(moves) - 1
    print("Amount of moves: " + str(amountOfMoves))
    msg = ""

    # The main loop.
    while (completedPuzzle == False):
        print("i is at " + str(joe))
        potentialFEN = puzzle.updateFEN(moves[joe+1][0], moves[joe+1][1], potentialFEN)
        # If we are at the last move.
        if joe+1 >= amountOfMoves:
            potentialFEN = puzzle.updateFEN(moves[-1][0], moves[-1][1], oldFEN)
            # If we got the correct move, end the loop.
            if reply == board.getPieceFromCoord(potentialFEN, moves[-1][1]):
                embed = discord.Embed(title="Puzzle complete!")
                embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
                await ctx.send(embed=embed)
                if os.path.exists("editedBoard.png"):
                    os.remove("editedBoard.png")
                print("Command executed succesfully.")
                return
        else:
            # If the player wants to execute a command.
            if reply.startswith(bot.command_prefix):
                print("Command executed succesfully.")
                print("Exiting out of the puzzle routine.")
                on_message(msg)
                return
            # If this is the beginning of the puzzle.
            elif reply == "INITIAL":
                lastMove = board.getPieceFromCoord(oldFEN, moves[0][1])
                requiredMove = board.getPieceFromCoord(potentialFEN, moves[joe+1][1])
                arr = puzzle.createPuzzleEmbed(oldFEN, lastMove, requiredMove, ctx, True, difficulty, str(puzzleData[7]))
                await ctx.send(file=arr[0], embed=arr[1])
            # If we got the correct move.
            elif reply == board.getPieceFromCoord(potentialFEN, moves[joe+1][1]):
                oldFEN = potentialFEN
                joe += 1
                potentialFEN = puzzle.clearSquare(moves[joe][0], potentialFEN)
                arr = puzzle.createCongratulationsEmbed(potentialFEN, ctx)
                await ctx.send(file=arr[0], embed=arr[1])
                joe += 1
                potentialFEN = puzzle.updateFEN(moves[joe][0], moves[joe][1], potentialFEN)
                potentialFEN = puzzle.clearSquare(moves[joe][0], potentialFEN)
                lastMove = board.getPieceFromCoord(potentialFEN, moves[joe][1])
                requiredMove = board.getPieceFromCoord(potentialFEN, moves[joe+1][1])
                arr = puzzle.createPuzzleEmbed(potentialFEN, lastMove, requiredMove, ctx, True, difficulty, str(puzzleData[7]))
                await ctx.send(file=arr[0], embed=arr[1])
            # If we didn't.
            else:
                print("the move is " + moves[joe][1])
                lastMove = board.getPieceFromCoord(oldFEN, moves[joe][1])
                requiredMove = board.getPieceFromCoord(potentialFEN, moves[joe+1][1])
                arr = puzzle.createPuzzleEmbed(oldFEN, lastMove, requiredMove, ctx, False, difficulty, str(puzzleData[7]))
                await ctx.send(file=arr[0], embed=arr[1])

        # Go and get the next message in the channel and use it as the reply.
        def check(m):
            return m.channel == channel and m.author.bot != True

        msg = await bot.wait_for('message', check=check)
        reply = msg.content

        # If the board image exists, delete it.
        if os.path.exists("editedBoard.png"):
            os.remove("editedBoard.png")
    return


# Links chess.com/lichess accounts to the Discord user.
@bot.command(name="link")
async def linkUser(ctx, platform, platname):
    username = ctx.author.name + "#" + ctx.author.discriminator
    with open("link.json") as file:
        data = json.load(file)
        existingEntryIndex = None
        for a in range(0, len(data["accounts"])):
            if data["accounts"][a]["username"] == username:
                existingEntryIndex = a
            else:
                pass
        if existingEntryIndex != None:
            data["accounts"][existingEntryIndex][platform] = platname
        else:
            data["accounts"].append({
                "username": username,
                platform: platname
            })
        with open("link.json", "w") as out:
            json.dump(data, out, indent=4)
        out.close()
        print("Linked " + platform + " account " + platname + " to " + username + ".")
        embed = discord.Embed(title="Link succesful", description="Linked " + platform + " account " + platname + " to " + username + ".")
        print("Command executed succesfully.")
        embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
        await ctx.channel.send(embed=embed)
    file.close()
    return

# Gets info about the chess.com/lichess accounts associated with the specified Discord user.
@bot.command(name="user")
async def getUser(ctx, mention: discord.Member):
    username = mention.name + "#" + mention.discriminator
    with open("link.json") as file:
        data = json.load(file)
        userInfo = None
        for a in range(0, len(data["accounts"])):
            if data["accounts"][a]["username"] == username:
                userInfo = data["accounts"][a]
            else:
                pass
        if userInfo != None:
            embed = discord.Embed(title=username + "'s " + "accounts")
            if "chesscom" in userInfo:
                platname = userInfo["chesscom"]
                stat = chesscom.getUserStat(platname).json
                embed.add_field(name="Chess.com", value="https://chess.com/member/" + platname, inline=False)
                embed.add_field(name="Bullet", value=stat["chess_bullet"]["last"]["rating"])
                embed.add_field(name="Blitz", value=stat["chess_blitz"]["last"]["rating"])
                embed.add_field(name="Rapid", value=stat["chess_bullet"]["last"]["rating"])
            if "lichess" in userInfo:
                platname = userInfo["lichess"]
                stat = lichess.getUser(platname)
                embed.add_field(name="Lichess.org", value="https://lichess.org/@/" + platname, inline=False)
                embed.add_field(name="Bullet", value=stat["perfs"]["bullet"]["rating"])
                embed.add_field(name="Blitz", value=stat["perfs"]["blitz"]["rating"])
                embed.add_field(name="Rapid", value=stat["perfs"]["rapid"]["rating"])
            embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
            await ctx.channel.send(embed=embed)
            print("Command executed succesfully.")
        else:
            embed = discord.Embed(title="Sorry!", description="Could not find the specified user in the database.")
            embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
            await ctx.channel.send(embed=embed)
            print("Command executed unsuccesfully.")
                
    return

# Gets info about the specified chess.com user.
@bot.command(name="chesscomuser")
async def getChesscomUser(ctx, username):
    if username == None:
        embed = discord.Embed(title="Sorry!", description="Was not given a user to search for.")
        embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
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
        embed.set_footer(text="Dates and times are in GMT. Developed by Verl#7647, GitHub: https://github.com/TheVerl")
        await ctx.channel.send(embed=embed)
        print("Command executed succesfully.")
    except:
        embed = discord.Embed(title="Sorry!", description="Could not find the specified user.")
        await ctx.channel.send(embed=embed)
        print("Command executed unsuccesfully.")
    return

# Gets info about the specified lichess user.
@bot.command(name="lichessuser")
async def getLichessUser(ctx, username):
    if username == None:
        embed = discord.Embed(title="Sorry!", description="Was not given a user to search for.")
        embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
        await ctx.channel.send(embed=embed)
        print("Command executed unsuccesfully.")
    try:
        data = (lichess.getUser(username))
    except:
        embed = discord.Embed(title="Sorry!", description="Could not find the specified user.")
        embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
        await ctx.channel.send(embed=embed)
        print("Command executed unsuccesfully.")
        return
    try:
        if (data['closed'] == True):
            embed = discord.Embed(title="Sorry!", description="The specified user's account has been closed.")
            embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
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
        embed.set_footer(text="Dates and times are in GMT. Developed by Verl#7647, GitHub: https://github.com/TheVerl")
        await ctx.channel.send(embed=embed)
        print("Command executed succesfully.")

def init():
    with open("discord.token") as f:
        token = f.read()
    f.close()
    bot.run(token)

if __name__ == '__main__':
    print("Loading...")
    init()
