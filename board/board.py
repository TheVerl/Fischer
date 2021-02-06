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
x = [ 25, 109, 194, 279, 363, 448, 531, 616 ]
y = [ 25, 109, 194, 279, 363, 448, 531, 616 ]

# Gets a peace in a FEN from a coordinate.
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

# Defines the directory of the image for the piece.
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

# Generates an image of a chess board from the FEN.
def generateImage(situation):
    boardImage = Image.open("board/board.png") 
    for fil in range(0, len(situation) - 1):
        for rank in range(0, len(situation[fil])):
            #print(situation[fil][rank].colour + " " + situation[fil][rank].piece)
            piece = definePiece(situation[fil][rank])
            if piece is None: continue
            truePiece = Image.open(piece).convert("RGBA")
            #truePiece = truePiece.resize((75, 75))
            boardImage.paste(truePiece, (x[rank], y[fil]), truePiece)
            #print("pasted " + boardDict[fil][rank].colour + " " + boardDict[fil][rank].piece)
                
    boardImage.save("editedBoard.png")
    return