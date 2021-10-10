from blessed import Terminal
from pathlib import Path
import json
import random
import sys

import blessed

class ChessPiece:

    def __init__(self, player, type, first_move = False, moved_recently = False, location = None):
        self.player = player
        self.type = type

        # this is stored as a string
        self.location = location

        # whether the piece has ever been moved (used for pawns)
        self.first_move = first_move

        # whether the piece made a move recently (tracking en passant for pawns)
        self.moved_recently = moved_recently
    
class Board:
    
    def __init__(self):
        # list comprehension that creates a list of lists to make a 2d board
        self.board_array = [ [ChessPiece(0, "space") for _ in range(8) ] for _ in range(8)]

        self.populate()

    # sets up the chess pieces on the board
    def populate(self):
        for i in range(8):
            self.board_array[i][1] = ChessPiece(1, "pawn", location=str(i) + "1")
            self.board_array[i][6] = ChessPiece(2, "pawn", location=str(i) + "6")

        self.board_array[0][0] = ChessPiece(1, "rook", location="00")
        self.board_array[7][0] = ChessPiece(1, "rook", location="70")
        self.board_array[0][7] = ChessPiece(2, "rook", location="07")
        self.board_array[7][7] = ChessPiece(2, "rook", location="77")

        self.board_array[1][0] = ChessPiece(1, "knight", location="10")
        self.board_array[6][0] = ChessPiece(1, "knight", location="60")
        self.board_array[1][7] = ChessPiece(2, "knight", location="17")
        self.board_array[6][7] = ChessPiece(2, "knight", location="67")

        self.board_array[2][0] = ChessPiece(1, "bishop", location="20")
        self.board_array[5][0] = ChessPiece(1, "bishop", location="50")
        self.board_array[2][7] = ChessPiece(2, "bishop", location="27")
        self.board_array[5][7] = ChessPiece(2, "bishop", location="57")

        self.board_array[3][0] = ChessPiece(1, "queen", location="30")
        self.board_array[3][7] = ChessPiece(2, "queen", location="37")

        # king
        self.board_array[4][0] = ChessPiece(1, "x", location="40")
        self.board_array[4][7] = ChessPiece(2, "x", location="47")

    # print out the current state of the board
    def show_board(self, term, option="default", moving_piece=None, valid_moves=None):
        print(term.red_on_gray60(" abcdefgh "))

        for y in reversed(range(len(self.board_array))):
            print(term.red_on_gray60(str(y + 1)), end="")

            for x in range(len(self.board_array[y])):
                if option == "show_move" and (str(x) + str(y)) == moving_piece.location:
                        if self.board_array[x][y].player == 1:
                            print(term.snow_on_red(self.board_array[x][y].type.upper()[0]), end="")
                        elif self.board_array[x][y].player == 2:
                            print(term.black_on_red(self.board_array[x][y].type.upper()[0]), end="")
                elif option == "show_move" and any(move.move == (str(x) + str(y)) for move in valid_moves):
                    if self.board_array[x][y].player == 1:
                        print(term.snow_on_cyan(self.board_array[x][y].type.upper()[0]), end="")
                    elif self.board_array[x][y].player == 2:
                        print(term.black_on_cyan(self.board_array[x][y].type.upper()[0]), end="")
                    else:
                        print(term.red_on_cyan(" "), end="")
                else:
                    if x % 2 == y % 2:
                        if self.board_array[x][y].player == 1:
                            print(term.snow_on_orange4(self.board_array[x][y].type.upper()[0]), end="")
                        elif self.board_array[x][y].player == 2:
                            print(term.black_on_orange4(self.board_array[x][y].type.upper()[0]), end="")
                        else:
                            print(term.orange4_on_orange4(" "), end="")
                    else:
                        if self.board_array[x][y].player == 1:
                            print(term.snow_on_orange3(self.board_array[x][y].type.upper()[0]), end="")
                        elif self.board_array[x][y].player == 2:
                            print(term.black_on_orange3(self.board_array[x][y].type.upper()[0]), end="")
                        else:
                            print(term.orange3_on_orange3(" "), end="")
                    
            print(term.red_on_gray60(str(y + 1)), end="")
            print("")
        print(term.red_on_gray60(" abcdefgh "), end="")
        print("\n")

    def move_piece(self, start_location, end_location, player):
        # if there is a piece at the start location that belongs to the player
        if self.board_array[int(start_location[0])][int(start_location[1])].player == player:
            pass
            #print("You have a piece here")
        else:
            #print("You don't have a piece here")
            return

        # mark that the piece has been moved before
        if self.board_array[int(start_location[0])][int(start_location[1])].first_move == False:
            #print("first move")
            self.board_array[int(start_location[0])][int(start_location[1])].first_move = True

        # clear moved_recently from previously moved pieces
        for x in range(8):
            for y in range(8):
                if self.board_array[x][y].moved_recently == True:
                    self.board_array[x][y].moved_recently = False

        # if a pawn moved two spaces
        if abs(int(start_location[1]) - int(end_location[1])) > 1 and self.board_array[int(start_location[0])][int(start_location[1])].type == "pawn":
            #print("a pawn moved two spaces")
            # mark that the piece has been moved recently
            self.board_array[int(start_location[0])][int(start_location[1])].moved_recently = True

        # update location
        self.board_array[int(start_location[0])][int(start_location[1])].location = end_location[0] + end_location[1]

        # copy the piece to its new location
        self.board_array[int(end_location[0])][int(end_location[1])] = self.board_array[int(start_location[0])][int(start_location[1])]
        # set empty space where the chess piece used to be
        self.board_array[int(start_location[0])][int(start_location[1])] = ChessPiece(0, "space")


# stores a chess move, and whether this move captures a piece
class Move():
    def __init__(self, new_move, new_captured_piece, new_captured_location):
        self.move = new_move
        self.captured_piece = new_captured_piece
        self.captured_location = new_captured_location



def convert_position_to_index(position):
    letter_to_index = {letter: num for letter, num in zip('abcdefgh', range(8))}
    # raise Exception("Invalid position")
    index = str(letter_to_index[position[0]]) + str((int(position[1]) - 1))
    return index


# converts a move command to two board array indices
def parse_move(input_move):
    return [convert_position_to_index(pos) for pos in input_move.split(" to ")]

# returns valid move positions for a given chess piece
def find_valid_moves(chess_piece, board, start_position):
    valid_moves = []

    if chess_piece.type == "pawn":
        if chess_piece.player == 1:
            # if the pawn has never been moved before
            if chess_piece.first_move == False:
                # if there are no pieces within 2 spaces in front of the pawn
                if board.board_array[int(start_position[0])][int(start_position[1]) + 1].type == "space" and board.board_array[int(start_position[0])][int(start_position[1]) + 2].type == "space":
                    #valid_moves.append((start_position[0] + str(int(start_position[1]) + 2)))
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + 2), None, None))

            # can move forward?
            if int(start_position[1]) + 1 < 8 and board.board_array[int(start_position[0])][int(start_position[1]) + 1].type == "space":
                #valid_moves.append((start_position[0] + str(int(start_position[1]) + 1)))
                valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + 1), None, None))

            # can attack en passant?
            if int(start_position[1]) + 1 < 8: # if there is room to move forward

                if int(start_position[0]) > 0: # if there is room to the left
                    # if there is an enemy pawn to the left and it is vulnerable to en passant
                    if board.board_array[int(start_position[0]) - 1][int(start_position[1])].player == 2 and \
                    board.board_array[int(start_position[0]) - 1][int(start_position[1])].type == "pawn" and \
                    board.board_array[int(start_position[0]) - 1][int(start_position[1])].moved_recently == True:
                        #print("en passant attack possible")
                        #valid_moves.append(str(int(start_position[0]) - 1) + str(int(start_position[1]) + 1))
                        valid_moves.append(Move(str(int(start_position[0]) - 1) + str(int(start_position[1]) + 1),\
                        board.board_array[int(start_position[0]) - 1][int(start_position[1])],\
                        str(int(start_position[0]) - 1) + start_position[1]))
                    # can attack diagonally left? 
                    elif board.board_array[int(start_position[0]) - 1][int(start_position[1]) + 1].type != "space":
                        #valid_moves.append(str(int(start_position[0]) - 1) + str(int(start_position[1]) + 1))
                        valid_moves.append(Move(str(int(start_position[0]) - 1) + str(int(start_position[1]) + 1),\
                        board.board_array[int(start_position[0]) - 1][int(start_position[1]) + 1],\
                        str(int(start_position[0]) - 1) + str(int(start_position[1]) + 1)))
            
                if int(start_position[0]) < 7: # if there is room to the right
                    # if there is an enemy pawn to the right and it is vulnerable to en passant
                    if board.board_array[int(start_position[0]) + 1][int(start_position[1])].player == 2 and \
                    board.board_array[int(start_position[0]) + 1][int(start_position[1])].type == "pawn" and \
                    board.board_array[int(start_position[0]) + 1][int(start_position[1])].moved_recently == True:
                        #print("en passant attack possible")
                        #valid_moves.append(str(int(start_position[0]) + 1) + str(int(start_position[1]) + 1))
                        valid_moves.append(Move(str(int(start_position[0]) + 1) + str(int(start_position[1]) + 1),\
                        board.board_array[int(start_position[0]) + 1][int(start_position[1])],\
                        str(int(start_position[0]) + 1) + start_position[1]))
                    # can attack diagonally right? 
                    elif board.board_array[int(start_position[0]) + 1][int(start_position[1]) + 1].type != "space":
                        #valid_moves.append(str(int(start_position[0]) + 1) + str(int(start_position[1]) + 1))
                        valid_moves.append(Move(str(int(start_position[0]) + 1) + str(int(start_position[1]) + 1),\
                        board.board_array[int(start_position[0]) + 1][int(start_position[1]) + 1],\
                        str(int(start_position[0]) + 1) + str(int(start_position[1]) + 1)))
            

        else:
            # if the pawn has never been moved before
            if chess_piece.first_move == False:
                # if there are no pieces within 2 spaces in front of the pawn
                if board.board_array[int(start_position[0])][int(start_position[1]) - 1].type == "space" and board.board_array[int(start_position[0])][int(start_position[1]) - 2].type == "space":
                    #valid_moves.append((start_position[0] + str(int(start_position[1]) - 2)))
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) - 2), None, None))

            # can move forward?
            if int(start_position[1]) - 1 > 0 and board.board_array[int(start_position[0])][int(start_position[1]) - 1].type == "space":
                #valid_moves.append((start_position[0] + str(int(start_position[1]) - 1)))
                valid_moves.append(Move(start_position[0] + str(int(start_position[1]) - 1), None, None))

            # can attack en passant?
            if int(start_position[1]) - 1 > 0: # if there is room to move forward

                if int(start_position[0]) > 0: # if there is room to the left
                    # if there is an enemy pawn to the left and it is vulnerable to en passant
                    if board.board_array[int(start_position[0]) - 1][int(start_position[1])].player == 1 and \
                    board.board_array[int(start_position[0]) - 1][int(start_position[1])].type == "pawn" and \
                    board.board_array[int(start_position[0]) - 1][int(start_position[1])].moved_recently == True:
                        #print("en passant attack possible")
                        #valid_moves.append(str(int(start_position[0]) - 1) + str(int(start_position[1]) - 1))
                        valid_moves.append(Move(str(int(start_position[0]) - 1) + str(int(start_position[1]) - 1),\
                        board.board_array[int(start_position[0]) - 1][int(start_position[1])],\
                        str(int(start_position[0]) - 1) + start_position[1]))

                    # can attack diagonally left? 
                    elif board.board_array[int(start_position[0]) - 1][int(start_position[1]) - 1].type != "space":
                        #valid_moves.append(str(int(start_position[0]) - 1) + str(int(start_position[1]) - 1))
                        valid_moves.append(Move(str(int(start_position[0]) - 1) + str(int(start_position[1]) - 1),\
                        board.board_array[int(start_position[0]) - 1][int(start_position[1]) - 1],\
                        str(int(start_position[0]) - 1) + str(int(start_position[1]) - 1)))
            
                if int(start_position[0]) < 7: # if there is room to the right
                    # if there is an enemy pawn to the right and it is vulnerable to en passant
                    if board.board_array[int(start_position[0]) + 1][int(start_position[1])].player == 1 and \
                    board.board_array[int(start_position[0]) + 1][int(start_position[1])].type == "pawn" and \
                    board.board_array[int(start_position[0]) + 1][int(start_position[1])].moved_recently == True:
                        #print("en passant attack possible")
                        #valid_moves.append(str(int(start_position[0]) + 1) + str(int(start_position[1]) - 1))
                        valid_moves.append(Move(str(int(start_position[0]) + 1) + str(int(start_position[1]) - 1),\
                        board.board_array[int(start_position[0]) + 1][int(start_position[1])],\
                        str(int(start_position[0]) + 1) + start_position[1]))

                    # can attack diagonally right? 
                    elif board.board_array[int(start_position[0]) + 1][int(start_position[1]) - 1].type != "space":
                        #valid_moves.append(str(int(start_position[0]) + 1) + str(int(start_position[1]) - 1))
                        valid_moves.append(Move(str(int(start_position[0]) + 1) + str(int(start_position[1]) - 1),\
                        board.board_array[int(start_position[0]) + 1][int(start_position[1]) - 1],\
                        str(int(start_position[0]) + 1) + str(int(start_position[1]) - 1)))

    elif chess_piece.type == "knight":
        # can move extreme upper left?
        if int(start_position[0]) > 0 and int(start_position[1]) < 5:
            if board.board_array[int(start_position[0]) - 1][int(start_position[1]) + 2].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) - 1) + str(int(start_position[1]) + 2), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) - 1][int(start_position[1]) + 2].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) - 1) + str(int(start_position[1]) + 2),\
                board.board_array[int(start_position[0]) - 1][int(start_position[1]) + 2],\
                str(int(start_position[0]) - 1) + str(int(start_position[1]) + 2)))
        # can move upper left?
        if int(start_position[0]) > 1 and int(start_position[1]) < 7:
            if board.board_array[int(start_position[0]) - 2][int(start_position[1]) + 1].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) - 2) + str(int(start_position[1]) + 1), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) - 2][int(start_position[1]) + 1].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) - 2) + str(int(start_position[1]) + 1),\
                board.board_array[int(start_position[0]) - 2][int(start_position[1]) + 1],\
                str(int(start_position[0]) - 2) + str(int(start_position[1]) + 1)))
        # can move lower left?
        if int(start_position[0]) > 1 and int(start_position[1]) > 0:
            if board.board_array[int(start_position[0]) - 2][int(start_position[1]) - 1].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) - 2) + str(int(start_position[1]) - 1), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) - 2][int(start_position[1]) - 1].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) - 2) + str(int(start_position[1]) - 1),\
                board.board_array[int(start_position[0]) - 2][int(start_position[1]) - 1],\
                str(int(start_position[0]) - 2) + str(int(start_position[1]) - 1)))
        # can move extreme lower left?
        if int(start_position[0]) > 0 and int(start_position[1]) > 2:
            if board.board_array[int(start_position[0]) - 1][int(start_position[1]) - 2].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) - 1) + str(int(start_position[1]) - 2), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) - 1][int(start_position[1]) - 2].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) - 1) + str(int(start_position[1]) - 2),\
                board.board_array[int(start_position[0]) - 1][int(start_position[1]) - 2],\
                str(int(start_position[0]) - 1) + str(int(start_position[1]) - 2)))

        # can move extreme upper right?
        if int(start_position[0]) < 7 and int(start_position[1]) < 5:
            if board.board_array[int(start_position[0]) + 1][int(start_position[1]) + 2].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) + 1) + str(int(start_position[1]) + 2), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) + 1][int(start_position[1]) + 2].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) + 1) + str(int(start_position[1]) + 2),\
                board.board_array[int(start_position[0]) + 1][int(start_position[1]) + 2],\
                str(int(start_position[0]) + 1) + str(int(start_position[1]) + 2)))
        # can move upper right?
        if int(start_position[0]) < 6 and int(start_position[1]) < 7:
            if board.board_array[int(start_position[0]) + 2][int(start_position[1]) + 1].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) + 2) + str(int(start_position[1]) + 1), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) + 2][int(start_position[1]) + 1].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) + 2) + str(int(start_position[1]) + 1),\
                board.board_array[int(start_position[0]) + 2][int(start_position[1]) + 1],\
                str(int(start_position[0]) + 2) + str(int(start_position[1]) + 1)))
        # can move lower right?
        if int(start_position[0]) < 6 and int(start_position[1]) > 0:
            if board.board_array[int(start_position[0]) + 2][int(start_position[1]) - 1].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) + 2) + str(int(start_position[1]) - 1), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) + 2][int(start_position[1]) - 1].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) + 2) + str(int(start_position[1]) - 1),\
                board.board_array[int(start_position[0]) + 2][int(start_position[1]) - 1],\
                str(int(start_position[0]) + 2) + str(int(start_position[1]) - 1)))
        # can move extreme lower right?
        if int(start_position[0]) < 7 and int(start_position[1]) > 2:
            if board.board_array[int(start_position[0]) + 1][int(start_position[1]) - 2].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) + 1) + str(int(start_position[1]) - 2), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) + 1][int(start_position[1]) - 2].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) + 1) + str(int(start_position[1]) - 2),\
                board.board_array[int(start_position[0]) + 1][int(start_position[1]) - 2],\
                str(int(start_position[0]) + 1) + str(int(start_position[1]) - 2)))

    # elif chess_piece.type == "rook":
    #     horizontal_or_vertical = 0
    #     neg_pos = 1

    #     for x in range(4):
    #         if x > 1:
    #             horizontal_or_vertical = 1
            
    #         for i in range(1, 8):
    #             if horizontal_or_vertical == 0:
                
    #                 if int(start_position[0]) + i < 8:
    #                     if board.board_array[int(start_position[0]) + neg_pos * i][int(start_position[1])].type == "space":
    #                         valid_moves.append(Move(str(int(start_position[0]) + neg_pos * i) + start_position[1], None, None))
    #                     # can attack?    
    #                     elif board.board_array[int(start_position[0]) + neg_pos * i][int(start_position[1])].player != chess_piece.player:
    #                         valid_moves.append(Move(str(int(start_position[0]) + neg_pos * i) + start_position[1],\
    #                         board.board_array[int(start_position[0]) + neg_pos * i][int(start_position[1])],\
    #                         str(int(start_position[0]) + neg_pos * i) + start_position[1]))
    #                         break
    #                     else:
    #                         break
    #                 else:
    #                     break
    #             elif horizontal_or_vertical == 1:
    #                 # room to move up?
    #                 if int(start_position[1]) + i < 8:
    #                     if board.board_array[int(start_position[0])][int(start_position[1]) + neg_pos * i].type == "space":
    #                         valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + neg_pos * i), None, None))
    #                     # can attack?    
    #                     elif board.board_array[int(start_position[0])][int(start_position[1]) + neg_pos * i].player != chess_piece.player:
    #                         valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + neg_pos * i),\
    #                         board.board_array[int(start_position[0])][int(start_position[1]) + neg_pos * i],\
    #                         str(int(start_position[0])) + str(int(start_position[1]) + neg_pos * i)))
    #                         break
    #                     else:
    #                         break
    #                 else:
    #                     break

    #         if neg_pos == 1:
    #             neg_pos = -1
    #         else:
    #             neg_pos = 1


    elif chess_piece.type == "rook":
        for i in range(1, 8):
            # room to move right?
            if int(start_position[0]) + i < 8:
                if board.board_array[int(start_position[0]) + i][int(start_position[1])].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) + i) + start_position[1], None, None))
                # can attack?    
                elif board.board_array[int(start_position[0]) + i][int(start_position[1])].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) + i) + start_position[1],\
                    board.board_array[int(start_position[0]) + i][int(start_position[1])],\
                    str(int(start_position[0]) + i) + start_position[1]))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move left?
            if int(start_position[0]) - i > 0:
                if board.board_array[int(start_position[0]) - i][int(start_position[1])].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) - i) + start_position[1], None, None))
                # can attack?    
                elif board.board_array[int(start_position[0]) - i][int(start_position[1])].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) - i) + start_position[1],\
                    board.board_array[int(start_position[0]) - i][int(start_position[1])],\
                    str(int(start_position[0]) - i) + start_position[1]))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move up?
            if int(start_position[1]) + i < 8:
                if board.board_array[int(start_position[0])][int(start_position[1]) + i].type == "space":
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + i), None, None))
                # can attack?    
                elif board.board_array[int(start_position[0])][int(start_position[1]) + i].player != chess_piece.player:
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + i),\
                    board.board_array[int(start_position[0])][int(start_position[1]) + i],\
                    str(int(start_position[0])) + str(int(start_position[1]) + i)))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move down?
            if int(start_position[1]) - i > 0:
                if board.board_array[int(start_position[0])][int(start_position[1]) - i].type == "space":
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) - i), None, None))
                # can attack?    
                elif board.board_array[int(start_position[0])][int(start_position[1]) - i].player != chess_piece.player:
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) - i),\
                    board.board_array[int(start_position[0])][int(start_position[1]) - i],\
                    str(int(start_position[0])) + str(int(start_position[1]) - i)))
                    break
                else:
                    break
            else:
                break


    elif chess_piece.type == "bishop":
        for i in range(1, 8):
            # room to move upper right?
            if int(start_position[0]) + i < 8 and int(start_position[1]) + i < 8:
                if board.board_array[int(start_position[0]) + i][int(start_position[1]) + i].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) + i), None, None))
                # can attack?
                elif board.board_array[int(start_position[0]) + i][int(start_position[1]) + i].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) + i),\
                    board.board_array[int(start_position[0]) + i][int(start_position[1]) + i],\
                    str(int(start_position[0]) + i) + str(int(start_position[1]) + i)))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move upper left?
            if int(start_position[0]) - i > 0 and int(start_position[1]) + i < 8:
                if board.board_array[int(start_position[0]) - i][int(start_position[1]) + i].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) + i), None, None))
                # can attack?
                elif board.board_array[int(start_position[0]) - i][int(start_position[1]) + i].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) + i),\
                    board.board_array[int(start_position[0]) - i][int(start_position[1]) + i],\
                    str(int(start_position[0]) - i) + str(int(start_position[1]) + i)))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move lower right?
            if int(start_position[0]) + i < 8 and int(start_position[1]) - i > 0:
                if board.board_array[int(start_position[0]) + i][int(start_position[1]) - i].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) - i), None, None))
                # can attack?
                elif board.board_array[int(start_position[0]) + i][int(start_position[1]) - i].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) - i),\
                    board.board_array[int(start_position[0]) + i][int(start_position[1]) - i],\
                    str(int(start_position[0]) + i) + str(int(start_position[1]) - i)))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move lower left?
            if int(start_position[0]) - i > 0 and int(start_position[1]) - i > 0:
                if board.board_array[int(start_position[0]) - i][int(start_position[1]) - i].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) - i), None, None))
                # can attack?
                elif board.board_array[int(start_position[0]) - i][int(start_position[1]) - i].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) - i),\
                    board.board_array[int(start_position[0]) - i][int(start_position[1]) - i],\
                    str(int(start_position[0]) - i) + str(int(start_position[1]) - i)))
                    break
                else:
                    break
            else:
                break

    elif chess_piece.type == "queen":
        # check cross moves
        for i in range(1, 8):
            # room to move right?
            if int(start_position[0]) + i < 8:
                if board.board_array[int(start_position[0]) + i][int(start_position[1])].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) + i) + start_position[1], None, None))
                # can attack?    
                elif board.board_array[int(start_position[0]) + i][int(start_position[1])].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) + i) + start_position[1],\
                    board.board_array[int(start_position[0]) + i][int(start_position[1])],\
                    str(int(start_position[0]) + i) + start_position[1]))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move left?
            if int(start_position[0]) - i > 0:
                if board.board_array[int(start_position[0]) - i][int(start_position[1])].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) - i) + start_position[1], None, None))
                # can attack?    
                elif board.board_array[int(start_position[0]) - i][int(start_position[1])].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) - i) + start_position[1],\
                    board.board_array[int(start_position[0]) - i][int(start_position[1])],\
                    str(int(start_position[0]) - i) + start_position[1]))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move up?
            if int(start_position[1]) + i < 8:
                if board.board_array[int(start_position[0])][int(start_position[1]) + i].type == "space":
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + i), None, None))
                # can attack?    
                elif board.board_array[int(start_position[0])][int(start_position[1]) + i].player != chess_piece.player:
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + i),\
                    board.board_array[int(start_position[0])][int(start_position[1]) + i],\
                    str(int(start_position[0])) + str(int(start_position[1]) + i)))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move down?
            if int(start_position[1]) - i > 0:
                if board.board_array[int(start_position[0])][int(start_position[1]) - i].type == "space":
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) - i), None, None))
                # can attack?    
                elif board.board_array[int(start_position[0])][int(start_position[1]) - i].player != chess_piece.player:
                    valid_moves.append(Move(start_position[0] + str(int(start_position[1]) - i),\
                    board.board_array[int(start_position[0])][int(start_position[1]) - i],\
                    str(int(start_position[0])) + str(int(start_position[1]) - i)))
                    break
                else:
                    break
            else:
                break

        # check diagonal moves
        for i in range(1, 8):
            # room to move upper right?
            if int(start_position[0]) + i < 8 and int(start_position[1]) + i < 8:
                if board.board_array[int(start_position[0]) + i][int(start_position[1]) + i].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) + i), None, None))
                # can attack?
                elif board.board_array[int(start_position[0]) + i][int(start_position[1]) + i].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) + i),\
                    board.board_array[int(start_position[0]) + i][int(start_position[1]) + i],\
                    str(int(start_position[0]) + i) + str(int(start_position[1]) + i)))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move upper left?
            if int(start_position[0]) - i > 0 and int(start_position[1]) + i < 8:
                if board.board_array[int(start_position[0]) - i][int(start_position[1]) + i].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) + i), None, None))
                # can attack?
                elif board.board_array[int(start_position[0]) - i][int(start_position[1]) + i].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) + i),\
                    board.board_array[int(start_position[0]) - i][int(start_position[1]) + i],\
                    str(int(start_position[0]) - i) + str(int(start_position[1]) + i)))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move lower right?
            if int(start_position[0]) + i < 8 and int(start_position[1]) - i > 0:
                if board.board_array[int(start_position[0]) + i][int(start_position[1]) - i].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) - i), None, None))
                # can attack?
                elif board.board_array[int(start_position[0]) + i][int(start_position[1]) - i].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) - i),\
                    board.board_array[int(start_position[0]) + i][int(start_position[1]) - i],\
                    str(int(start_position[0]) + i) + str(int(start_position[1]) - i)))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            # room to move lower left?
            if int(start_position[0]) - i > 0 and int(start_position[1]) - i > 0:
                if board.board_array[int(start_position[0]) - i][int(start_position[1]) - i].type == "space":
                    valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) - i), None, None))
                # can attack?
                elif board.board_array[int(start_position[0]) - i][int(start_position[1]) - i].player != chess_piece.player:
                    valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) - i),\
                    board.board_array[int(start_position[0]) - i][int(start_position[1]) - i],\
                    str(int(start_position[0]) - i) + str(int(start_position[1]) - i)))
                    break
                else:
                    break
            else:
                break

    # king
    elif chess_piece.type == "x":
        i = 1
        # check cross moves

        # room to move right?
        if int(start_position[0]) + i < 8:
            if board.board_array[int(start_position[0]) + i][int(start_position[1])].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) + i) + start_position[1], None, None))
            # can attack?    
            elif board.board_array[int(start_position[0]) + i][int(start_position[1])].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) + i) + start_position[1],\
                board.board_array[int(start_position[0]) + i][int(start_position[1])],\
                str(int(start_position[0]) + i) + start_position[1]))


        # room to move left?
        if int(start_position[0]) - i > 0:
            if board.board_array[int(start_position[0]) - i][int(start_position[1])].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) - i) + start_position[1], None, None))
            # can attack?    
            elif board.board_array[int(start_position[0]) - i][int(start_position[1])].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) - i) + start_position[1],\
                board.board_array[int(start_position[0]) - i][int(start_position[1])],\
                str(int(start_position[0]) - i) + start_position[1]))


        # room to move up?
        if int(start_position[1]) + i < 8:
            if board.board_array[int(start_position[0])][int(start_position[1]) + i].type == "space":
                valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + i), None, None))
            # can attack?    
            elif board.board_array[int(start_position[0])][int(start_position[1]) + i].player != chess_piece.player:
                valid_moves.append(Move(start_position[0] + str(int(start_position[1]) + i),\
                board.board_array[int(start_position[0])][int(start_position[1]) + i],\
                str(int(start_position[0])) + str(int(start_position[1]) + i)))


        # room to move down?
        if int(start_position[1]) - i > 0:
            if board.board_array[int(start_position[0])][int(start_position[1]) - i].type == "space":
                valid_moves.append(Move(start_position[0] + str(int(start_position[1]) - i), None, None))
            # can attack?    
            elif board.board_array[int(start_position[0])][int(start_position[1]) - i].player != chess_piece.player:
                valid_moves.append(Move(start_position[0] + str(int(start_position[1]) - i),\
                board.board_array[int(start_position[0])][int(start_position[1]) - i],\
                str(int(start_position[0])) + str(int(start_position[1]) - i)))

        # check diagonal moves

        # room to move upper right?
        if int(start_position[0]) + i < 8 and int(start_position[1]) + i < 8:
            if board.board_array[int(start_position[0]) + i][int(start_position[1]) + i].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) + i), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) + i][int(start_position[1]) + i].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) + i),\
                board.board_array[int(start_position[0]) + i][int(start_position[1]) + i],\
                str(int(start_position[0]) + i) + str(int(start_position[1]) + i)))


        # room to move upper left?
        if int(start_position[0]) - i > 0 and int(start_position[1]) + i < 8:
            if board.board_array[int(start_position[0]) - i][int(start_position[1]) + i].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) + i), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) - i][int(start_position[1]) + i].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) + i),\
                board.board_array[int(start_position[0]) - i][int(start_position[1]) + i],\
                str(int(start_position[0]) - i) + str(int(start_position[1]) + i)))


        # room to move lower right?
        if int(start_position[0]) + i < 8 and int(start_position[1]) - i > 0:
            if board.board_array[int(start_position[0]) + i][int(start_position[1]) - i].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) - i), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) + i][int(start_position[1]) - i].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) + i) + str(int(start_position[1]) - i),\
                board.board_array[int(start_position[0]) + i][int(start_position[1]) - i],\
                str(int(start_position[0]) + i) + str(int(start_position[1]) - i)))


        # room to move lower left?
        if int(start_position[0]) - i > 0 and int(start_position[1]) - i > 0:
            if board.board_array[int(start_position[0]) - i][int(start_position[1]) - i].type == "space":
                valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) - i), None, None))
            # can attack?
            elif board.board_array[int(start_position[0]) - i][int(start_position[1]) - i].player != chess_piece.player:
                valid_moves.append(Move(str(int(start_position[0]) - i) + str(int(start_position[1]) - i),\
                board.board_array[int(start_position[0]) - i][int(start_position[1]) - i],\
                str(int(start_position[0]) - i) + str(int(start_position[1]) - i)))


    return valid_moves

# returns True or False depending on whether the supplied move is valid
def validateMove(board, move):
    valid_moves = find_valid_moves(board.board_array[int(move[0][0])][int(move[0][1])], board, move[0])

    for i in valid_moves:
        if i.move == move[1]:
            return True
    return False

def easy_bot(board, whoseTurn):
    piece_list = []

    # scan board for own pieces
    for x in range(8):
        for y in range(8):
            if board.board_array[x][y].player == whoseTurn:
                board.board_array[x][y].location = str(x) + str(y)
                piece_list.append(board.board_array[x][y])

    #for i in piece_list:
        #print(i.location + " " + i.type)

    while True:
        # pick a piece at random
        try_piece = random.choice(piece_list)

        if len(find_valid_moves(try_piece, board, try_piece.location)) > 0:
            # pick a valid move at random
            move = random.choice(find_valid_moves(try_piece, board, try_piece.location))
            break
    
    move_list = []
    move_list.append(try_piece.location)
    move_list.append(move.move)
    return move_list

def play_vs_bot(my_path, term):
    my_board = Board()
    move_history = []

    whose_turn = 1

    my_board.show_board(term)

    while True:
        if whose_turn == 1:
            print("\nIt is player " + str(whose_turn) + "'s turn")


            input_move = input("Enter your move. (Example: a2 to a4) Or enter option for options\n")
            if input_move == "option":
                option = input("Enter an option: history, save\n")
                if option == "history":
                    for i in move_history:
                        print(i)
                if option == "save":
                    save_dictionary = {}
                    save_dictionary["moveHistory"] = move_history
                    with open(my_path / "saved_game.json", "w") as outfile:
                        json.dump(save_dictionary, outfile, indent=4)
                continue

            parsed_moves = parse_move(input_move)
        else:
            print("\nIt is the bot's turn.")
            parsed_moves = easy_bot(my_board, whose_turn)
            print("easy bot moved " + my_board.board_array[int(parsed_moves[0][0])][int(parsed_moves[0][1])].type)

        if validateMove(my_board, parsed_moves) != True:
            print("Invalid move!")
            continue

        move_history.append(input_move)

        my_board.show_board(term, moving_piece=my_board.board_array[int(parsed_moves[0][0])][int(parsed_moves[0][1])], option="show_move",\
        valid_moves=find_valid_moves(my_board.board_array[int(parsed_moves[0][0])][int(parsed_moves[0][1])], my_board, my_board.board_array[int(parsed_moves[0][0])][int(parsed_moves[0][1])].location))

        my_board.move_piece(parsed_moves[0], parsed_moves[1], whose_turn)

        my_board.show_board(term)

        # update whose turn it is
        if whose_turn == 1:
            whose_turn = 2
        else:
            whose_turn = 1

def echo_yx(cursor, text):
    """Move to ``cursor`` and display ``text``."""
    print(cursor.term.move_yx(cursor.y, cursor.x) + text)

# checks if each player stil has their king
def check_for_win(board):
    p1_alive = False
    p2_alive = False

    for y in range(len(board.board_array)):
        for x in range(len(board.board_array[y])):
            if board.board_array[x][y].type == "x" and board.board_array[x][y].player == 1:
                p1_alive = True
            if board.board_array[x][y].type == "x" and board.board_array[x][y].player == 2:
                p2_alive = True
    
    if p1_alive == False:
        return "p2_win"

    if p2_alive == False:
        return "p1_win"

    return "ongoing"




def main():
    # blessed terminal
    term = Terminal()
    my_board = Board()

    my_path = Path.home() / "danielb-project0"

    move_history = []
    save_dictionary = {}

    whose_turn = 1

    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            with open(sys.argv[2]) as infile:
                save_dictionary = json.load(infile)
            move_history = save_dictionary["moveHistory"]
            for i in move_history:
                parsed_moves = parse_move(i)
                found_moves = find_valid_moves(my_board.board_array[int(parsed_moves[0][0])][int(parsed_moves[0][1])], my_board, parsed_moves[0])
                for x in found_moves:
                    print(x.move)
                my_board.move_piece(parsed_moves[0], parsed_moves[1], whose_turn)
                # update whose turn it is
                if whose_turn == 1:
                    whose_turn = 2
                else:
                    whose_turn = 1
            if check_for_win(my_board) == "p1_win":
                sys.exit(0)
            sys.exit(1)

    easy_bot(my_board, 2)

    my_board.show_board(term)

    print("Welcome to Chess\n")
    option = input("Enter 1 to start new game, Enter 2 to load a saved game\n")

    # load a game
    if option == "2":
        with open(my_path / "saved_game.json") as infile:
            save_dictionary = json.load(infile)
        move_history = save_dictionary["moveHistory"]
        for i in move_history:
            parsed_moves = parse_move(i)
            found_moves = find_valid_moves(my_board.board_array[int(parsed_moves[0][0])][int(parsed_moves[0][1])], my_board, parsed_moves[0])
            for x in found_moves:
                print(x.move)
            my_board.move_piece(parsed_moves[0], parsed_moves[1], whose_turn)
            # update whose turn it is
            if whose_turn == 1:
                whose_turn = 2
            else:
                whose_turn = 1


    my_board.show_board(term)

    option = input("Enter 1 for player vs player, Enter 2 to play against easy bot\n")
    if option == "2":
        play_vs_bot(my_path, term)

    while True:
        print("\nIt is player " + str(whose_turn) + "'s turn")
        input_move = input("Enter your move. (Example: a1 to a3) Or enter option for options\n")
        if input_move == "option":
            option = input("Enter an option: history, save\n")
            if option == "history":
                for i in move_history:
                    print(i)
            if option == "save":
                save_dictionary = {}
                save_dictionary["moveHistory"] = move_history
                with open(my_path / "saved_game.json", "w") as outfile:
                    json.dump(save_dictionary, outfile, indent=4)
            continue

        parsed_moves = parse_move(input_move)

        if validateMove(my_board, parsed_moves) != True:
            print("Invalid move!")
            continue

        move_history.append(input_move)

        my_board.move_piece(parsed_moves[0], parsed_moves[1], whose_turn)
        my_board.show_board(term)

        # update whose turn it is
        if whose_turn == 1:
            whose_turn = 2
        else:
            whose_turn = 1


    pass

main()