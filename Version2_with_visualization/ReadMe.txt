Laser Project – Lazor Game


Group Members: Jana, Maya, Ranjan

A Python-based implementation of the classic Lazor game where lasers interact with reflective, refractive, and opaque blocks to reach target positions. Includes a solver and visualization.

Project Structure
lazor_game/
│
├── main.py              # Run the puzzle solver
├── laser.py             # Laser class (movement, reflection/refraction)
├── file_reader.py       # Reads .bff files and extracts grid/locations
├── solver.py            # Simulates lasers and finds solutions
├── visualizer.py        # Visualizes the grid and laser paths
└── bff/                 # Puzzle files (.bff)

Installation

Clone the repository:

git clone <repo_url>
cd lazor_game


Install dependencies:

pip install numpy matplotlib

How to Run

Place your .bff puzzle files in the bff/ folder.

Edit main.py to choose your puzzle:

bff = "./bff/tiny_5.bff"


Run the solver:

python main.py


Output:

Console: Laser paths and solution status.

Visualization: solution_visual.png saved in the project folder.

Block Types:
Block	Behavior
A	Reflective
B	Opaque (absorbs)
C	Refractive
o	Empty / Allowed location
x	Obstacles / Fixed

Features:

Simulates multiple lasers simultaneously.

Reflective, refractive, and opaque block logic.

Automatically checks all block permutations.

High-quality visual representation of laser paths.

Modular, easy-to-extend code.

Future Improvements:

Interactive GUI for manual block placement.

More complex laser mechanics (split beams, angled mirrors).

Optimized solver for large grids.

Multiple solution support and visualization.

License:

Educational use. Credit the authors if used.