#!/usr/bin/env python3

# Import modules
import discord 
from discord.ext import commands
import sys, json, datetime, csv, random, os, copy
from datetime import datetime

# Import scripts
sys.path.insert(0, 'board/')
import board

# Functions

# Creates an embed from a FEN, two moves and a context.
def createPuzzleEmbed(FEN, lastMove, requiredMove, ctx, correct, difficulty, themes):
    board.generateImage(FEN)
    print("MOVE REQUIRED: " + requiredMove)
    text = ""
    if correct == True:
        text = (FEN[-1][0] + " has played " + lastMove + ". Your turn.\nYou must send only algebraic notation of your move.")
    else:
        text = ("Incorrect, try again!\n" + FEN[-1][0] + " has played " + lastMove + ". Your turn.\nYou must send only algebraic notation of your move.")
    embed = discord.Embed(title="Random Puzzle\n" + difficulty + "\n" + themes, description=text)
    file = discord.File("editedBoard.png", filename="image.png")
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
    return [file, embed]

# Create's an embed when the player does the correct move.
def createCongratulationsEmbed(FEN, ctx):
    board.generateImage(FEN)
    embed = discord.Embed(title="Correct!")
    file = discord.File("editedBoard.png", filename="image.png")
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text="Developed by Verl#7647, GitHub: https://github.com/TheVerl")
    return [file, embed]

# Parses a raw FEN string and then sends it to the decompiler to format it properly.
def parseFEN(rawFEN):
    FEN = []
    gameData = []
    for x in range(0, len(rawFEN)):
        if (x != len(rawFEN) - 1):
            FEN.append(rawFEN[x])
        else:
            FEN.append(rawFEN[x].split(" ", 1)[0])
            gameData = rawFEN[x].split(" ")

    print("FEN:")
    for x in range(0, len(FEN)):
        print(FEN[x])
    print("\n")
    print("Extra data:")
    for x in range(1, len(gameData)):
        print(gameData[x])
    print("\n")

    FEN = decompileFEN(FEN, gameData)
    return FEN

# Clears a square.
def clearSquare(coord, situation):
    situationCopy = copy.deepcopy(situation)
    coordArray = [char for char in coord]
    fil = int(ord(coordArray[0]) - 96) - 1
    rank = 8 - int(coordArray[1])
    situationCopy[rank][fil].piece = "none"
    situationCopy[rank][fil].colour = "empty"
    return situationCopy

# Moves a piece in a FEN to a new location, playing out a move.
def updateFEN(oldCoord, newCoord, situation):
    situationCopy = copy.deepcopy(situation)
    coordArray = [char for char in oldCoord]
    oldFil = int(ord(coordArray[0]) - 96) - 1
    oldRank = 8 - int(coordArray[1])
    piece = situationCopy[oldRank][oldFil].piece
    colour = situationCopy[oldRank][oldFil].colour
    coordArray = [char for char in newCoord]
    fil = int(ord(coordArray[0]) - 96) - 1
    rank = 8 - int(coordArray[1])
    situationCopy[rank][fil].piece = piece
    situationCopy[rank][fil].colour = colour
    if (situationCopy[-1][0] == "white"):
        situationCopy[-1][0] = "black"
    elif (situationCopy[-1][0] == "black"):
        situationCopy[-1][0] = "white"
    return situationCopy

# Formats the parsed FEN into a suitable form.
def decompileFEN(fen, data):
    situation = []
    for x in range(0, len(fen)):
        row = [char for char in fen[x]]
        line = []
        for y in range(0, len(row)):
            if row[y].isnumeric():
                for z in range(int(row[y])):
                    line.append(board.Square("empty", "none"))
            else:
                colour = ""
                piece = ""
                if row[y].isupper():
                    colour = "white"
                else:
                    colour = "black"
                if (row[y].lower() == "r"):
                    piece = "rook"
                elif (row[y].lower() == "n"):
                    piece = "knight"
                elif (row[y].lower() == "b"):
                    piece = "bishop"
                elif (row[y].lower() == "q"):
                    piece = "queen"
                elif (row[y].lower() == "k"):
                    piece = "king"
                elif (row[y].lower() == "p"):
                    piece = "pawn"
                line.append(board.Square(colour, piece))
        situation.append(line)
    
    extra = []
    if (data[1] == "w"):
        extra.append("White")
    elif (data[1] == "b"):
        extra.append("Black")

    # Add castling and other stuff the end of the FEN describes later lol

    situation.append(extra)
    
    return situation