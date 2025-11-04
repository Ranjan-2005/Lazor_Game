import matplotlib.pyplot as plt
import numpy as np
from file_reader import Locations

def visualize_puzzle(grid, list_of_lasers, points, mesh):
    """
    Plots the grid, laser paths, and target points, then saves the visualization as a PNG file.

    Parameters:
        grid (ndarray): The grid to visualize.
        list_of_lasers (list of Laser objects): All laser objects to plot.
        points (list of tuple of int): Target points that lasers must hit.

    Returns:
        None
    """
    def plot_scatter(data, marker, size, color):
        if data.size:
            plt.scatter(data[:, 1], data[:, 0], marker=marker, s=size, color=color)
            
    # Get locations of all blocks in given puzzle
    o = np.array(Locations(grid, 'o'))
    A = np.array(Locations(grid, 'A'))
    B = np.array(Locations(grid, 'B'))
    C = np.array(Locations(grid, 'C'))
    x = np.array(Locations(grid, 'x'))
    fixedA = np.array(Locations(mesh, 'A'))
    fixedB = np.array(Locations(mesh, 'B'))
    fixedC = np.array(Locations(mesh, 'C'))

    # Plot puzzle to visualize
    f = plt.figure()
    # Plot fixed blocks on the grid
    plot_scatter(o, 's', 5000, "#F4E866") # darkgray
    plot_scatter(A, 's', 5000, "#84D7E9") # blue
    plot_scatter(B, 's', 5000, "#FA8220") # orange
    plot_scatter(C, 's', 5000, "#BC52BC") # light purple
    plot_scatter(x, 's', 5000, "#A59807") # gray
    # Plot fixed blocks on the mesh
    plot_scatter(fixedA, 'o', 1000, "#11C9F2") # dark blue
    plot_scatter(fixedB, 'o', 1000, "#944707") # dark orange
    plot_scatter(fixedC, 'o', 1000, '#800080') # dark purple

    # Target points
    points = np.array(points)
    for s in [100, 70, 30, 10]:
        plt.scatter(points[:, 1], points[:, 0], color='dimgrey', s=s, edgecolor='black')

    # Laser routes
    for l in list_of_lasers:
        for i in range(len(l.coordinates) - 1):
            xPoints = l.coordinates[i][0], l.coordinates[i + 1][0]
            yPoints = l.coordinates[i][1], l.coordinates[i + 1][1]
            plt.plot(yPoints, xPoints, color='red')
        # Plot starting point with different markers for refracted lasers
        if not l.refract:
            plt.scatter(l.coordinates[0][1], l.coordinates[0][0], color='red', s=100, edgecolor='orange')
            plt.scatter(l.coordinates[0][1], l.coordinates[0][0], color='red', s=20, edgecolor='pink')

    # Add specific coordinate reference points
    # Point (0,0) - Origin
    plt.text(0, 0, '(0,0)', fontsize=10, ha='center', va='center',
             color='yellow', weight='bold',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.8))

    # Point (1,0)
    plt.text(1, 0, '(1,0)', fontsize=10, ha='center', va='center',
             color='yellow', weight='bold',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.8))

    # Point (0,1)
    plt.text(0, 1, '(0,1)', fontsize=10, ha='center', va='center',
             color='yellow', weight='bold',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.8))

    # Set plot aesthetics
    plt.rcParams['figure.facecolor'] = 'dimgrey'
    x, y = grid.shape
    plt.xlim(0, y - 1)
    plt.ylim(0, x - 1)
    f.set_figwidth(y - 3)
    f.set_figheight(x - 3)
    plt.grid()
    plt.axis('off')

    # Save puzzle as png
    plt.savefig("solution_visual.png")
