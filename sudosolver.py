################################################################################
# Author:   Evan Dietrich
# Course:   Comp 131 - Intro AI
# Prof:     Santini
#
# Assign:   Constraint Satisfaction Problems
# Date:     10/28/2020
# File:     sudosolver.py
################################################################################

################################################################################
#       IMPORTS + INITIALS FOR TESTING
################################################################################

FILENAME = "hardpuzzle.txt"     # Alternatively, "easypuzzle.txt"
ALGORITHM = "BACKTRACKING"      # Alternatively, BACKJUMPING
import sys
import copy
import os
import math
import numpy as np
import time

################################################################################
#       ConstraintSatisfaction Class: Runs BACKTRACK or BACKJUMP as given
################################################################################

class ConstraintSatisfaction(object):

    # General solver function, launches backtrack or backjump based on globals
    def solver(self, sudoku):
        coords = []
        for x in range(0, 9):
            for y in range(0, 9):
                if sudoku.puzzle[x][y] == 0:
                    coords.append((x, y))

        if ALGORITHM == "BACKTRACKING":
            return self.backtrack(sudoku, sudoku.puzzle, coords)
        elif ALGORITHM == "BACKJUMPING":
            return self.backjump(sudoku, sudoku.puzzle, coords)

    # Backtrack algorithm based on pseudocode in Lecture 07 [CSP Pg. 23]
    def backtrack(self, sudoku, puzzle, coords):
        if len(coords) == 0: return True, puzzle

        # Assign subsequent coords
        row_after, column_after = coords[0]
        coords_after = coords[1:]

        # Recursive approach, updating puzzle board as needed
        for x in range(1, 10):
            if sudoku.checkCoords(puzzle, row_after, column_after, x):
                puzzle[row_after, column_after] = x
                result, update_puzzle = self.backtrack(sudoku, puzzle.copy(), coords_after)
                
                if result: return True, update_puzzle
                puzzle[row_after, column_after] = 0

        return False, puzzle

    # Backjump algorithm, attempted to follow flow of diagrams in Lecture 07 
    # [CSP Pg. 41-53] Ran into issues while attempting to "migrate" by variables
    # Instead settled on modifiying general backjump approach to try & simulate
    def backjump(self, sudoku, puzzle, coords):
        if len(coords) == 0: return True, puzzle, set()

        # Conflict set tracking new conflicting assignments + subsequent coords
        conflict_set = set()
        row_after, column_after = coords[0]
        coords_after = coords[1:]

        # Observing board
        for x in range(1, 10):
            result = False
            update_puzzle = []
            # Requires set conflicts in conflict-driven backjump approach
            new_conflicts = set()
            if sudoku.checkCoords(puzzle, row_after, column_after, x):
                puzzle[row_after, column_after] = x
                result, update_puzzle, new_conflicts = self.backjump(sudoku, puzzle.copy(), coords_after)
            else:
                new_conflicts = sudoku.checkConflicts(puzzle, row_after, column_after, x)

            # Attempts to return immediately after conflict, may not have been
            # adjusted properly from general backjump pseudocode reference point
            if result: return True, update_puzzle, set()
            elif (row_after + (8 * column_after)) not in new_conflicts:
                return False, puzzle, new_conflicts
            else:
                new_conflicts.remove(row_after + (8 * column_after))
                conflict_set = conflict_set.union(new_conflicts)

            # return updated puzzle
            puzzle[row_after, column_after] = 0

        return False, puzzle, conflict_set


################################################################################
#       SUDOKU Class: Provides layout & check steps for board as necessary
#       A "solved" sudoku puzzle requires unique numbers within Subsquares,
#       rows, columns, as well as ensuring that no conflicts arise between
#       each of the 9 unique SubSquares. Thus, we must check this continually.
################################################################################

class Sudoku(object):

    # Initial vals
    def __init__(self, puzzle, constraint_approach):
        self.puzzle = puzzle
        self.constraint_approach = constraint_approach

    # Essentially calls the general solver in ConstraintSatisfaction Class
    def solver(self):
        coords = []
        for x in range(0, 9):
            for y in range(0, 9):
                if self.puzzle[x][y] == 0:
                    coords.append((x, y))
        return self.constraint_approach.solver(self)

    # Ensures general line is valid
    def checkLine(self, axis, index, puzzle):
        line = []
        if axis == 0:
            line = puzzle[index, :]
        elif axis == 1:
            line = puzzle[:, index]
        return is_valid

    # When called, ensures the 3x3 SubSquare is valid (used in all 9 of puzzle)
    def checkSubSquare(self, row, column, puzzle):
        line = []
        for x in range(0,3):
            for y in range(0, 3):
                line.append(puzzle[(row + x), (column + y)])
        is_valid = self.checkLine(line)
        return is_valid

    # Check gen X/Y axes of Board validity
    def checkAxes(self, puzzle, axis, axis_index, num):
        for x in range(0, 9):
            if axis == 0:
                if (puzzle[axis_index][x] == num):
                    return True
            elif axis == 1:
                if (puzzle[x][axis_index] == num):
                    return True
        return False

    # Check if number already used in 
    def checkIfUsed(self, puzzle, row, column, num):
        for x in range(3):
            for y in range(3):
                if (puzzle[x + row][y + column] == num):
                    return True
        return False

    # Confirms Puzzle has been solved or not by observing each row/col/SubSquare
    def checkDone(self, puzzle):
        for x in range(0, 9):
            if not self.checkLine(0, x, puzzle):
                return False
            if not self.checkLine(1, x, puzzle):
                return False

            row = (int(x / 3)) * 3
            column = (x % 3) * 3
            if not self.checkSubSquare(row, column, puzzle):
                return False

        if (0 not in puzzle):
            return False

        return True

    # Same but for X/Y Coords of Board validity
    def checkCoords(self, arr, row, column, num):
        return not self.checkIfUsed(arr, row - row % 3, column - column % 3, num) and \
               not self.checkAxes(arr, 0, row, num) and \
               not self.checkAxes(arr, 1, column, num)

    # Check rows, then columns, for conflict set pairings
    def checkConflicts(self, puzzle, row, column, num):
        conflict_set = set()
        for x in range(9):
            if puzzle[row][x] == num:
                conflict_set.add((row + (x * 8)))
        for x in range(9):
            if puzzle[x][column] == num:
                conflict_set.add((x + (column * 8)))

        box_row = row - row % 3 #TODO: Check Python order of operations
        box_column = column - column % 3

        # Update lastest to conflict set after determination & return to
        # backjump in ConstraintSatisfaction Class 
        for x in range(3):
            for y in range(3):
                if (puzzle[x + box_row][y + box_column] == num):
                    conflict_set.add(x + box_row + (8 * (y + box_column)))
        conflict_set.add(row + (8 * column))
        return conflict_set


################################################################################
#       HELPER/PRINT FUNCTION ONCE DONE TO PROVIDE USER W/SOLUTION
################################################################################

def printBoard(board):
    print("---------------")
    for x in range(len(board)):
        if (x % 3 == 0) and (x != 0):
            print('---------------')
        for y in range(len(board[0])):
            if (y % 3 == 0) and (y != 0):
                print(' | ', end="")
            if y == 8:
                print(board[x][y]) 
            else :
                print(str(board[x][y]) + "", end="")
    print("---------------\n")

################################################################################
#       MAIN PROGRAM
################################################################################

if __name__ == '__main__':

    print("\n>>> SudoSolver\nFILE: " + FILENAME + "\nALGO: " + ALGORITHM + "\n")
    board = []

    # Read in txt file as long as it's in your current directory
    with open(FILENAME) as f:
        for line in f:
            temp_list = [int(elt.strip()) for elt in line.split(',')]
            board.append(temp_list)
    board = np.array(board)
    # tic = time.perf_counter()
    sudoku = Sudoku(board, ConstraintSatisfaction())
    final = ((sudoku.solver()[1:])[0]).tolist()
    # toc = time.perf_counter()
    printBoard(final)

    # Compare speed of solution from 2 algos for analysis in README.md
    # print(f"Solved with {toc - tic:0.4f} seconds")


