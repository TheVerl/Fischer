#!/usr/bin/env python3

# Import modules
from PIL import Image
import sys, os, copy

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Class
class Square:
    def __init__(self, colour, piece):
        self.colour = colour
        self.piece = piece

# Global variables
boardImage = Image.open("board/board.png")
x = [ 25, 109, 194, 279, 363, 448, 531, 616 ]
y = [ 25, 109, 194, 279, 363, 448, 531, 616 ]

def getPieceFromCoord(situation, coord):
    coordArray = [char for char in coord]
    fil = int(ord(coordArray[0]) - 96) - 1
    rank = 8 - int(coordArray[1])

    if (situation[rank][fil].piece == "king"):
        return "K" + coord
    elif (situation[rank][fil].piece == "queen"):
        return "Q" + coord
    elif (situation[rank][fil].piece == "rook"):
        return "R" + coord
    elif (situation[rank][fil].piece == "knight"):
        return "N" + coord
    elif (situation[rank][fil].piece == "bishop"):
        return "B" + coord
    elif (situation[rank][fil].piece == "pawn"):
        return coord
    else:
        return "how tf did this happen lmao"

def clearSquare(coord, situation):
    situationCopy = copy.deepcopy(situation)
    coordArray = [char for char in coord]
    fil = int(ord(coordArray[0]) - 96) - 1
    rank = 8 - int(coordArray[1])
    situationCopy[rank][fil].piece = "none"
    situationCopy[rank][fil].colour = "empty"
    return situationCopy

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

def decompileFEN(fen, data):
    situation = []
    for x in range(0, len(fen)):
        row = [char for char in fen[x]]
        line = []
        for y in range(0, len(row)):
            if row[y].isnumeric():
                for z in range(int(row[y])):
                    line.append(Square("empty", "none"))
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
                line.append(Square(colour, piece))
        situation.append(line)
    
    extra = []
    if (data[1] == "w"):
        extra.append("White")
    elif (data[1] == "b"):
        extra.append("Black")

    # Add castling and other stuff the end of the FEN describes later lol

    situation.append(extra)
    
    return situation

def definePiece(coord):
    chessman = ""
    if coord.colour == "empty":
        return None
    elif coord.colour == "white":
        chessman += "board/pieces/white/"
    elif coord.colour == "black":
        chessman += "board/pieces/black/"

    if coord.piece == "none":
        return None
    elif coord.piece == "king":
        chessman += "king.png"
    elif coord.piece == "queen":
        chessman += "queen.png"
    elif coord.piece == "rook":
        chessman += "rook.png"
    elif coord.piece == "knight":
        chessman += "knight.png"
    elif coord.piece == "bishop":
        chessman += "bishop.png"
    elif coord.piece == "pawn":
        chessman += "pawn.png"
    return chessman

def generateImage(situation):
    for fil in range(0, len(situation) - 1):
        for rank in range(0, len(situation[fil])):
            print(situation[fil][rank].colour + " " + situation[fil][rank].piece)
            piece = definePiece(situation[fil][rank])
            if piece is None: continue
            truePiece = Image.open(piece).convert("RGBA")
            #truePiece = truePiece.resize((75, 75))
            boardImage.paste(truePiece, (x[rank], y[fil]), truePiece)
            #print("pasted " + boardDict[fil][rank].colour + " " + boardDict[fil][rank].piece)
                
    boardImage.save("editedBoard.png")
    return