#!/usr/bin/env python3

# Import modules
from PIL import Image
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Class
class Square:
    def __init__(self, colour, piece):
        self.colour = colour
        self.piece = piece

# Global variables
boardImage = Image.open("board/board.png")
boardDict = [
    [ Square("black", "queen"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none") ],
    [ Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none") ],
    [ Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none") ],
    [ Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none") ],
    [ Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none") ],
    [ Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none"), Square("empty", "none") ]
]
x = [ 25, 109, 194, 279, 363, 448, 531, 616 ]
y = [ 616, 531, 448, 363, 279, 194, 109, 25 ]

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

def generateImage():
    for fil in range(0, len(boardDict)):
        for rank in range(0, len(boardDict[fil])):
            piece = definePiece(boardDict[fil][rank])
            if piece is None: continue
            truePiece = Image.open(piece).convert("RGBA")
            #truePiece = truePiece.resize((75, 75))
            boardImage.paste(truePiece, (rank, fil), truePiece)
                
    boardImage.save("editedBoard.png")
    return