import re
import numpy as np

def readbff(file_name):
    """
    Parses a Board File Format (.bff) file into a structured list representing
    the game grid, including lasers, blocks, and target positions.

    Parameters:
        file_name (str): The name of the '.bff' file to be read.

    Returns:
        list: A list containing the following elements:
            - The grid representing the placement of lasers and blocks.
            - numberOfBlocks (list): Counts of each block type (reflective, refractive, opaque).
            - laser_dict (dict): Information about lasers with keys 'laser_pos' and 'laser_dir'.
            - goalPositionsLocations (list): Coordinates of target points the lasers must hit.
    """
    # Open and read the content of the .bff file provided
    bff = open(file_name)
    read_bff = bff.read()
    # Extract the grid information using expressions
    grid_bounds = 'GRID START.*GRID STOP'  # any character between string grid start and grid stop, as per bff files
    grid = re.search(grid_bounds, read_bff, re.DOTALL)  # make the dot in the regular expression match any character
    grid_lines = read_bff[grid.start():grid.end()]  # Once the match is found, assign the substring in read_bff

    # Grid size calculation; x_dim and y_dim
    x_dim = 0
    # Extract rows from grid_lines, remove leading/trailing whitespace, and skip the first and last rows
    row_list = grid_lines.strip().split('\n')[1:-1]
    y_dim = len(row_list)
    # Extract variables (A, B, C, o, x) from the .bff file
    variables = re.search('([ABCox] *)+[ABCox]', read_bff)  # with or without spaces after
    # Get the substring of read_bff that matches the variables pattern
    variables = read_bff[variables.start():variables.end()]
    # Count the number of columns (x_dim) based on valid variables
    for i in variables:
        if i in ['A', 'B', 'C', 'o', 'x']:
            x_dim += 1
    # Create a 2D array to represent the full grid
    full_grid = [[0 for _ in range(2 * x_dim + 1)]  # Initialize a 2D array with zeros
        for _ in range(2 * y_dim + 1)]  # Specify the dimensions based on rows and columns
    # Loop through each row in row_list
    for row_index, row in enumerate(row_list):
        # Increment the row index
        grid_row = 2 * row_index + 1
        # Initialize the column index
        grid_col = 0

        # Loop through each character in the current row
        for cell in row:
            # Check if the character is not a space
            if cell != ' ':
                # Increment the column index for non-space characters
                grid_col += 1

                # Assign the non-space character to the corresponding position in the full_grid
                full_grid[grid_row][2 * grid_col - 1] = cell
    # Extract additional info from the .bff file
    miscellaneous = read_bff[:grid.start()] + read_bff[grid.end() + 1:]  # anything before or after grid start/stop
    # Split the additional info into a list of lines
    extra_list = miscellaneous.split('\n')
    # Initialize lists and counters
    goalPositionsLocations = []
    laser_loc = []
    laser_grad = []
    numberOfBlocks = [0]*3  # can be A, B, or C
    # Process the extracted info
    for line in extra_list:
        # Remove leading/trailing whitespaces from each line
        info = line.strip()
        # Skip empty lines
        if not info:
            continue
        # Identify the type of information (point, laser, block)
        identifier = info[0]
        # Split the data part of the line
        data = info[1:].strip().split(' ')
        if identifier == 'P':
            # Process point data
            point = (int(data[0]), int(data[1]))  # Converts the data to a tuple of int representing coordinates (x, y)
            goalPositionsLocations.append(point)
        elif identifier == 'L':
            # Process laser data, tuples of ints: one for the location (x, y) and one for the gradient (dx, dy)
            location = (int(data[0]), int(data[1]))
            gradient = (int(data[2]), int(data[3]))
            laser_loc.append(location)
            laser_grad.append(gradient)
        elif identifier in {'A', 'B', 'C'}:
            # Process block data
            index = ord(identifier) - ord('A')  # Convert letter to block index (0 for A, 1 for B, 2 for C)
            numberOfBlocks[index] = int(data[0])

    # Create a dictionary to store laser information
    laser_dict = {'laser_pos': laser_loc, 'laser_dir': laser_grad}
    # Return the results as a list
    return [np.array(full_grid), numberOfBlocks, laser_dict, goalPositionsLocations]

def Locations(grid, value):
    """
    Finds and returns all locations in the grid where a specified value occurs.

    Parameters:
        grid (ndarray of int): The grid read from the .bff file.
        value: The value to search for within the grid.

    Returns:
        list of tuple: A list of coordinates representing every location where the value is found.
    """
    # Use list comprehension to create a list of tuples representing the locations
    # where the specified value is found in the grid
    return [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == value]
