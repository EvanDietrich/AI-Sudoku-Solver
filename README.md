**********************************
Author:   Evan Dietrich
Course:   Comp 131 - Intro AI
Prof:     Santini

Assign:   Constraint Satisfaction Problems
Date:     10/28/2020
File:     README.md
**********************************

Overview:
This program implements a Sudoku puzzle solver using a Constraint Satisfaction
Problems approach. 

Technical Breakdown:
sudosolver.py   - Runs the program.  
README.md       - Instructions to run program and assignment overview.
easypuzzle.txt  - "Easy" Sudoku Puzzle
hardpuzzle.txt  - "Hard" Sudoku Puzzle

Running the Program:
To run the program, ensure all downloaded files are on your machine, and run
"python3 sudosolver.py" on your terminal screen. This will start the program
for a automated running procedure. The procedure given is controlled by the two
variables at the top of the 'sudosolver.py' file, as an example:

FILENAME = "hardpuzzle.txt"
ALGORITHM = BACKTRACKING

By editing the values of FILENAME (Modify the sudoku file choice) and of
ALGORITHM (BACKTRACKING or BACKJUMPING), you can test the sudoku solver model in
different scenarios, and observe the execution of the search procedure. Please
ensure the required ".txt" files are in the same directory as the program to
avoid file I/O issues.

BACKTRACKING:: Recursive Backtracking Search, based on Lecture 07 pseudocode.
BACKJUMPING:: Recursive Conflict-Directed Backjumping Search, based on Lecture 
07 simulated diagrams of Genearl Backjumping, with issues in trying to "migrate"
by variable and build sets based on individual variables.

Collaborators:
I completed this assignment with assistance from the student posts and
instructor answers on the Comp131 Piazza page, with the lecture material,
our class textbook, and a chapter from the following textbook:
"https://www.ics.uci.edu/~dechter/books/chapter06.pdf", which provided addt'l
pseudocode examples for implemenation of Backjump attempt. I also have written
a sudoku solver program in prior CS courses at Tufts, and went back to this
prior codebase to see differences in algorithm approach and pull from the
thought process of testing for puzzle validity (specifically axes, subsquares,
and general X/Y lines).

Notes:
Contrary to hope, timing my backtrack algorithm yielded a solve time of
0.9349 seconds. The Spec noted that Conflict-directed Backjumping might be
possible to use, and if so to add an implementation of the technique to your
solution for a faster resolution of the problem. However, timing my backjump
algorithm yielded a solve time of 2.2810 seconds. This may be due to it not
being a true Conflict-directed Backjump as hoped even with modification, but
I was surprised that the space reduction regardless did not increase speed.
However, both approaches do solve both provided sudoku puzzles correctly.
