# !/usr/bin/env python
'''
Program Assignment a2 : Part2 : Write a Python program that plays Betsy
Assigned Team Members : Jack McShane & Harsha Upadhyay
Input Parameters :
        1. current player: w or b (w for white , b for black)
        2. current_state: current state of the board as a string of 64 characters
            e. g RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr
            . : an empty square
            P or p : a white or black Parakeet
            R or r : a white or black Robin
            N or n : a white or black Nighthawk
            Q or q : a white or black Quetzal
            K or k : a white or black Kingfisher
            B or b : a white or black Blue jay, in row-major order
        3. time_limit: a time limit in seconds
Rules :
        8 X 8 square board
        Each player has sixteen pieces : 8 Parakeets, 2 Robins, 2 Nighthawks, 2 Blue jays, 1 Quetzal, and 1 Kingfisher
        The two players alternate turns, with White going first.
Move rule for each piece type:
        • A Parakeet may move one square forward, if no other piece is on that square. Or, a Parakeet may
        move one square forward diagonally (one square forward and one square left or right) if a piece of the
        opposite player is on that square, in the process capturing that piece from the board. If a Parakeet
        reaches the far row of the board (closest to the opposite player), it is transformed into a Quetzal. On
        its very first move of the game, a Parakeet may move forward two squares as long as both are empty.
        (Note that due to the rules of the game and the initial game state (see below), you can tell if a Parakeet
        has never been moved based on its position: a P (white Parakeet) that has not been moved will be in
        the second row of the board, and a p (black Parakeet) will be in the seventh row of the board.)
        • A Robin may move any number of squares either horizontally or vertically, landing on either an empty
        square or a piece of the opposite player (which is then captured), as long as all the squares between
        the starting and ending positions are empty.
        • A Blue jay is like a Robin, but moves along diagonal flight paths instead of horizontal or vertical ones.
        • A Quetzal is like a combination of a Robin and a Blue jay: it may move any number of empty squares
        horizontally, vertically, or diagonally, and land either on an empty square or on a piece of the opposite
        player (which is then captured).
        • A Kingfisher may move one square in any direction, horizontally or vertically, either to an empty square
        or to capture a piece of the opposing player.
        • A Nighthawk moves in L shaped patterns on the board, either two squares to the left or right followed
        by one square forward or backward, or one square left or right followed by two squares forward or 4
        backward. It may fly over any pieces on the way, but the destination square must either be empty or
        have a piece of the opposite player (which is then captured).

Notation :


Command line :
python3 ./betsy.py w RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr 10

Test Cases:

Code Reference Sources:
https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/
https://github.com/Dirk94/ChessAI
https://github.com/luweizhang/chess-ai/blob/master/ai/chessai.py
https://gist.github.com/rsheldiii/2993225
https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/

'''

import sys
import numpy as np
#from tkinter import Tk

# User inputs and initialization
in_current_player = str(sys.argv[1])
in_board_state = str(sys.argv[2])
in_time_limit = str(sys.argv[3])

#root = Tk()
if in_current_player == 'w':
    print("The computer is thinking...")
    #root.after(in_time_limit, ai_play(board))
else:
    print("You play as white.")
    #root.after(in_time_limit, player_play(board))

WHITE = "white"
BLACK = "black"


class Game:
    def __init__(self):
        self.playersturn = BLACK
        self.message = "Enter you move from one position to other"
        self.gameboard = {}
        self.placePieces()
        print("chess program. enter moves in algebraic notation separated by space")
        self.main()

    def placePieces(self):
        for i in range(0, 8):
            self.gameboard[(1,i)] = Parakeet(WHITE, input_d[WHITE][Parakeet], 1)
            self.gameboard[(6,i)] = Parakeet(BLACK, input_d[BLACK][Parakeet], -1)

        placers = [Robin, Nighthawk, Bluejay, Quetzal, Kingfisher, Bluejay, Nighthawk, Robin]

        for i in range(0, 8):
            self.gameboard[(0,i)] = placers[i](WHITE, input_d[WHITE][placers[i]])
            self.gameboard[(7,(7 - i))] = placers[i](BLACK, input_d[BLACK][placers[i]])
        placers.reverse()

    def main(self):

        while True:
            self.printBoard()
            #print(self.message)
            self.message = ""
            print("(Hey, human, in the time it takes you to read this sentence, I’ll have considered")
            print("5 billion board positions. But it’s cute that you’re still trying to beat me...")
            print( "Enter you move from one position to other")
            startpos, endpos = self.parseInput()
            try:
                target = self.gameboard[startpos]
                print('New board')
            except:
                self.message = "could not find piece; index probably out of range"
                target = None

            if target:
                print("found " + str(target))
                if target.Color != self.playersturn:
                    self.message = "you aren't allowed to move that piece this turn"
                    continue
                if target.isValid(startpos, endpos, target.Color, self.gameboard):
                    self.message = "that is a valid move"
                    self.gameboard[endpos] = self.gameboard[startpos]
                    del self.gameboard[startpos]
                    self.isCheck()
                    if self.playersturn == BLACK:
                        self.playersturn = WHITE
                    else:
                        self.playersturn = BLACK
                else:
                    self.message = "invalid move" + str(target.availableMoves(startpos[0], startpos[1], self.gameboard))
                    print(target.availableMoves(startpos[0], startpos[1], self.gameboard))
            else:
                self.message = "there is no piece in that space"

    def isCheck(self):
        # ascertain where the kings are, check all pieces of opposing color against those kings, then if either get hit, check if its checkmate
        kingfisher = Kingfisher
        KingfisherDict = {}
        pieceDict = {BLACK: [], WHITE: []}
        for position, piece in self.gameboard.items():
            if type(piece) == Kingfisher:
                KingfisherDict[piece.Color] = position
            print(piece)
            pieceDict[piece.Color].append((piece, position))
        # white
        if self.canSeeKingfisher(KingfisherDict[WHITE], pieceDict[BLACK]):
            self.message = "White player is in check"
        if self.canSeeKingfisher(KingfisherDict[BLACK], pieceDict[WHITE]):
            self.message = "Black player is in check"

    def canSeeKingfisher(self, Kingfisherpos, piecelist):
        # checks if any pieces in piece list (which is an array of (piece,position) tuples) can see the Kingfisher in kingpos
        for piece, position in piecelist:
            if piece.isValid(position, Kingfisherpos, piece.Color, self.gameboard):
                return True

    def parseInput(self):
        try:
            a, b = input().split()
            a = ((ord(a[0]) - 97), int(a[1]) - 1)
            b = (ord(b[0]) - 97, int(b[1]) - 1)
            return (a, b)
        except:
            print("error decoding input. please try again")
            return ((-1, -1), (-1, -1))

    def printBoard(self):

        for i in range(0, 8):
            for j in range(0, 8):
                item = self.gameboard.get((i, j), ".")
                print(str(item) + ' ', end=" ")
            print()

class Piece:

    def __init__(self, color, name):
        self.name = name
        self.position = None
        self.Color = color

    def isValid(self, startpos, endpos, Color, gameboard):
        if endpos in self.availableMoves(startpos[0], startpos[1], gameboard, Color=Color):
            return True
        return False

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def availableMoves(self, x, y, gameboard):
        print("ERROR: no movement for base class")

    def AdNauseum(self, x, y, gameboard, Color, intervals):
        answers = []
        for xint, yint in intervals:
            xtemp, ytemp = x + xint, y + yint
            while self.isInBounds(xtemp, ytemp):
                target = gameboard.get((xtemp, ytemp), None)
                if target is None:
                    answers.append((xtemp, ytemp))
                elif target.Color != Color:
                    answers.append((xtemp, ytemp))
                    break
                else:
                    break

                xtemp, ytemp = xtemp + xint, ytemp + yint
        return answers

    def isInBounds(self, x, y):
        "checks if a position is on the board"
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False

    def noConflict(self, gameboard, initialColor, x, y):
        "checks if a single position poses no conflict to the rules of chess"
        if self.isInBounds(x, y) and (((x, y) not in gameboard) or gameboard[(x, y)].Color != initialColor): return True
        return False


chessCardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
chessDiagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


def NighthawkList(x, y, int1, int2):
    """sepcifically for the Robin, permutes the values needed around a position for noConflict tests"""
    return [(x + int1, y + int2), (x - int1, y + int2), (x + int1, y - int2), (x - int1, y - int2),
            (x + int2, y + int1), (x - int2, y + int1), (x + int2, y - int1), (x - int2, y - int1)]


def KingfisherList(x, y):
    return [(x + 1, y), (x + 1, y + 1), (x + 1, y - 1), (x, y + 1), (x, y - 1), (x - 1, y), (x - 1, y + 1),
            (x - 1, y - 1)]


class Nighthawk(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return [(xx, yy) for xx, yy in NighthawkList(x, y, 2, 1) if self.noConflict(gameboard, Color, xx, yy)]


class Robin(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals)


class Bluejay(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessDiagonals)


class Quetzal(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals + chessDiagonals)


class Kingfisher(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return [(xx, yy) for xx, yy in KingfisherList(x, y) if self.noConflict(gameboard, Color, xx, yy)]


class Parakeet(Piece):
    def __init__(self, color, name, direction):
        self.name = name
        self.Color = color
        # of course, the smallest piece is the hardest to code. direction should be either 1 or -1, should be -1 if the Parakeet is traveling "backwards"
        self.direction = direction


    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        answers = []
        if (x + self.direction, y + 1) in gameboard and self.noConflict(gameboard, Color,x + self.direction, y + 1): answers.append(
                (x + self.direction, y + 1))
        if (x + self.direction , y - 1 ) in gameboard and self.noConflict(gameboard, Color,x + self.direction , y - 1 ): answers.append(
                (x + self.direction , y - 1 ))
        if (x + self.direction , y ) not in gameboard and Color == self.Color: answers.append((x + self.direction , y ))  # the condition after the and is to make sure the non-capturing movement (the only fucking one in the game) is not used in the calculation of checkmate
        print(answers)
        return answers

input_d = {WHITE: {Parakeet: "P", Robin: "R", Nighthawk: "N", Bluejay: "B", Kingfisher: "K", Quetzal: "Q"},
           BLACK: {Parakeet: "p", Robin: "r", Nighthawk: "n", Bluejay: "b", Kingfisher: "k", Quetzal: "q"}}

Game()