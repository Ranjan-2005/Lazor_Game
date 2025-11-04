Lazor Solver Project --> Creators: Jana Almadani, Ranjan Mukherjee, Maya Beyler

The Lazor Solver Project is a Python-based program designed to automatically solve Lazor puzzle files (with the extension .bff). The program reads each puzzle file, determines the correct arrangement of blocks, and outputs the solved configuration as a readable text file. It can process multiple puzzles at once and creates a separate solution file for each board.

Project Structure --> The project is made up of several Python files that work together:
•	main.py controls the entire solving process. It runs the solver on every .bff file in the specified folder, displays the solution in the terminal, and saves each solution as a text file.
•	lazor_solver.py contains the main solving logic, including the algorithms that trace laser paths and determine how blocks reflect, absorb, or refract beams.
•	bff_parser.py reads and interprets the .bff puzzle files, converting them into usable data structures such as the grid, the lasers, and the targets.
•	visualize.py is an optional file used to generate visual representations of the puzzles. It is not required for the text-only version of the program.
•	blocks.py defines the different block types: ReflectBlock, OpaqueBlock, and RefractBlock.
•	beam.py manages the behavior of the laser beams as they move through the grid.
•	grid.py handles the grid layout, coordinates, and the placement of blocks.
•	utils.py contains helper functions that are shared by multiple parts of the program.
•	unit_test.py contains automated tests that check the functionality of the solver, parser, and output system to ensure that all components work correctly.

How to Run the Program --> To run the Lazor Solver:
1.	Place all of your .bff puzzle files in the same folder as the Python files.
(You can also change the folder path in the main.py file if your puzzles are located elsewhere.)
2.	Open a terminal or command prompt in that folder.
3.	Run the program by typing “python main.py”.

The solver will automatically read each puzzle file, determine a valid block arrangement, and print the results in the terminal. It will also create a new text file for each solved puzzle. For example, if one of your puzzles is called “dark_1.bff,” the solver will generate a file named “dark_1_solution.txt” containing the solution.

Output Description --> Each solution text file includes two sections.

The first section lists the block placements, showing which type of block was placed and at which coordinates. The second section displays the solved puzzle grid, with letters and symbols representing each cell.

In the grid:
•	“A” stands for a ReflectBlock (a mirror that redirects the laser).
•	“B” stands for an OpaqueBlock (a block that absorbs the laser).
•	“C” stands for a RefractBlock (a block that splits the laser).
•	“o” represents an open space.
•	“x” marks a cell where a block cannot be placed.
Each solution file is saved in the same folder as its corresponding .bff file.

Unit Testing --> 

This project includes an automated unit test file named unit_test.py. It uses Python’s built-in unittest framework to verify that the solver and related components function correctly. The test suite checks four main areas: that the grid is built properly when placing blocks, that .bff files are successfully parsed into grids, lasers, and targets, that the solver returns the correct data format containing both block placements and laser paths, and that the solution text file is properly created and includes the expected sections such as Placements and Final Grid.

To run the unit test, open a terminal in the project folder and execute the test file using the unittest module. When all tests pass, the program will display a message confirming that four tests were run and all passed successfully. This indicates that all core functions of the project are working as intended.

Additional Notes --> 
•	The solver automatically detects whether block coordinates are given as (x, y) or (row, column), so you don’t have to adjust the input format.
•	If your .bff files are stored in a different folder, you can change the folder path in the final line of main.py to point to that location.
•	Each solution file is written to the same directory as its corresponding puzzle file for easy access.
