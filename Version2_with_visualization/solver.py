from laser import Laser
from file_reader import Locations

from itertools import permutations, combinations
import numpy as np
from visualizer import visualize_puzzle

def solve_maze(customGrid, initialPositions, laserPath, goalPositions, blockingCell):
    """
    Simulates the movement of lasers on the grid and determines whether
    the target configuration can be achieved.

    Parameters:
        customGrid (ndarray): The grid populated with blocks to interact with lasers.
        initialPositions (list of tuple of int): Coordinates of the lasers.
        laserPath (list of tuple of int): Direction vectors for each laser.
        goalPositions (list of tuple of int): Target points that lasers must hit.
        blockingCell (int): Number of refractive blocks (C blocks) present.

    Returns:
        final_list_of_lasers (list of Laser objects): The laser objects after simulation.
        solution (bool): True if all targets are successfully hit, False otherwise.
    """

    final_list_of_lasers = []  # list of lasers that work
    list_of_lasers = []  # initialize laser possibilities
    num_lasers = len(initialPositions)
    num_refract_lasers = 0  # Initialize number of refracted lasers
    max_pos = 10 * max(customGrid.shape) ** 2  # Maximum number of positions allowed for a laser
    max_refract = num_lasers * blockingCell * max(customGrid.shape)  # prevent infinite loop

    # Initialize lasers
    for i in range(num_lasers):
        list_of_lasers.append(Laser(initialPositions[i], laserPath[i]))

    while len(list_of_lasers) > 0:
        current_laser = list_of_lasers[0]

        laserOB = current_laser.OutsideBoundary(customGrid.shape)
        constrained_laser = len(current_laser.coordinates) > max_pos
        laser_stuck_refract = num_refract_lasers > max_refract

        # Break if the laser is constrained or refracted laser limit is reached
        if constrained_laser or laser_stuck_refract:
            break

        if laserOB:
            final_list_of_lasers.append(list_of_lasers.pop(0))
        else:
            # Determine edge type (0 for vertical, 1 for horizontal)
            current_laser.edge = 0 if current_laser.x % 2 == 1 else 1 if current_laser.y % 2 == 1 else current_laser.edge

            # Determine the position of the block in the laser's path
            if current_laser.edge == 0:  # Vertical edge
                xBlock = current_laser.x
                yBlock = current_laser.y + 1 if current_laser.dy == 1 else current_laser.y - 1
            else:  # Horizontal edge
                yBlock = current_laser.y
                xBlock = current_laser.x + 1 if current_laser.dx == 1 else current_laser.x - 1

            # Check bounds for block position
            if not (0 <= xBlock < customGrid.shape[0] and 0 <= yBlock < customGrid.shape[1]):
                current_laser.movelaser()
                continue

            block = customGrid[xBlock, yBlock]

            if block == 'A':
                # Reflect block
                if current_laser.edge == 0:  # Vertical edge
                    current_laser.dy = -current_laser.dy
                else:  # Horizontal edge
                    current_laser.dx = -current_laser.dx

                # Check if laser hits another reflect block immediately
                xNew, yNew = current_laser.x, current_laser.y
                if (0 <= xNew < customGrid.shape[0] and 0 <= yNew < customGrid.shape[1] and
                        customGrid[xNew, yNew] == 'A'):
                    # Stop laser if between reflect blocks
                    final_list_of_lasers.append(list_of_lasers.pop(0))
                else:
                    # Move laser
                    current_laser.movelaser()

            elif block == 'C':
                # Refraction block - one beam continues, one beam reflects
                num_refract_lasers += 1

                # Create reflected beam (copy of current laser)
                reflected_laser = Laser((current_laser.x, current_laser.y),
                                        (current_laser.dx, current_laser.dy))
                reflected_laser.refract = True
                reflected_laser.edge = current_laser.edge

                # Apply reflection to the new beam
                if reflected_laser.edge == 0:  # Vertical edge
                    reflected_laser.dy = -reflected_laser.dy
                else:  # Horizontal edge
                    reflected_laser.dx = -reflected_laser.dx

                # Move both beams
                reflected_laser.movelaser()
                current_laser.movelaser()

                # Add reflected beam to the list
                list_of_lasers.append(reflected_laser)

            elif block == 'B':
                # Opaque block - stop laser
                final_list_of_lasers.append(list_of_lasers.pop(0))

            elif block in ['x', 'o', 0]:
                # Empty space - move laser
                current_laser.movelaser()
            else:
                # Unknown block type - move laser
                current_laser.movelaser()

    # Collect all positions from all lasers
    allPositions = []
    for finishedLaser in final_list_of_lasers:
        allPositions.extend(finishedLaser.coordinates)

    # Remove duplicates
    allPositions = list(set(allPositions))

    # Check if all goal positions are hit
    solution = all(p in allPositions for p in goalPositions)
    return final_list_of_lasers, solution

def solution(fptr):
    from file_reader import readbff
    meshGrid, blocks, laserData, checkpoints = readbff(fptr)
    """
    Reads a .bff file, simulates laser movement on the grid, and determines 
    whether a solution exists using the `solve_maze` function.

    Parameters:
        fptr (str): Path to the .bff file to read.

    Returns:
        solution_grid (ndarray): The grid configuration that solves the puzzle.
        solution_lasers (list of Laser objects): The lasers and their traversed paths in the solution.
        checkpoints (list of tuple of int): Coordinates of target points that must be hit.
    """
    meshGrid, blocks, laserData, checkpoints = readbff(fptr)
    # Transpose of checkpoints
    checkpoints = [i[::-1] for i in checkpoints]

    # Reverse the transpose
    laserPoints = laserData['laser_pos']
    laserPoints = [i[::-1] for i in laserPoints]
    laserDirs = laserData['laser_dir']
    laserDirs = [i[::-1] for i in laserDirs]

    # Possible blocks
    blockValues = ['A', 'B', 'C']
    blockList = []
    for i in range(3):
        for j in range(blocks[i]):
            blockList.append(blockValues[i])

    # Permuted block list
    permutedBlockList = [list(p) for p in set(permutations(blockList))] if blockList else None

    # Allowed locations
    allowedLocations = Locations(meshGrid, 'o')

    # Combination of allowed locations
    locationCombinations = [list(c) for c in combinations(allowedLocations, sum(blocks))]
    # Fill grid and solve
    for i in range(len(locationCombinations)):
        for j in range(len(permutedBlockList)):
            newGrid = meshGrid.copy()
            for k in range(sum(blocks)):
                newGrid[locationCombinations[i][k]] = permutedBlockList[j][k]
            traversedLaser, solutionValue = solve_maze(newGrid, laserPoints, laserDirs, checkpoints, blocks[2])
            if solutionValue:
                # Solution grid
                solution_grid = newGrid
                solution_lasers = traversedLaser
                break

    # Check solution and save
    visualize_puzzle(solution_grid, solution_lasers, checkpoints, meshGrid)
    return solution_grid, solution_lasers, checkpoints
