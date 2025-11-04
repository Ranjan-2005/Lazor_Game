
from lazor_simulator import LazorSim
from lazor_blocks import ReflectBlock, OpaqueBlock, RefractBlock
import itertools
import copy
from bff_parser import parse_bff

def solve_bff(file_path):
    parsed = parse_bff(file_path)
    return solve_board(parsed)
def solve_board(parsed):
    grid_template = parsed["grid"]
    lazors = parsed["lazors"]
    targets = parsed["targets"]
    blocks = parsed["blocks"]

    open_spaces = [(x, y) for y, row in enumerate(grid_template)
                   for x, cell in enumerate(row) if cell == "o"]

    block_list = (
        [ReflectBlock()] * blocks["A"] +
        [OpaqueBlock()] * blocks["B"] +
        [RefractBlock()] * blocks["C"]
    )

    for perm in itertools.permutations(block_list):
        for positions in itertools.permutations(open_spaces, len(block_list)):
            temp_grid = copy.deepcopy(grid_template)
            for (x, y), block in zip(positions, perm):
                temp_grid[y][x] = block
            sim = LazorSim(temp_grid, lazors, targets)
            if sim.simulate():
                # ✅ Patch: Return both block placement and paths
                return (
                    [(x, y, type(block).__name__) for (x, y), block in zip(positions, perm)],
                    sim.get_paths()  # ← make sure LazorSim has this method!
                )

    return None, []  # No solution found
