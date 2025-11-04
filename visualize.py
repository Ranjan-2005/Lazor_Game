
from PIL import Image, ImageDraw

CELL_SIZE = 60
MARGIN = 20

COLOR_MAP = {
    'ReflectBlock': 'blue',
    'OpaqueBlock': 'black',
    'RefractBlock': 'green',
    'empty': 'white',
    'gray': 'gray',
}

def draw_board(grid, blocks, lazors=None, filename="output.png"):
    rows = len(grid)
    cols = len(grid[0])
    width = cols * CELL_SIZE + 2 * MARGIN
    height = rows * CELL_SIZE + 2 * MARGIN

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Draw base grid
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            top_left = (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE)
            bottom_right = (top_left[0] + CELL_SIZE, top_left[1] + CELL_SIZE)

            block_type = 'empty'
            if isinstance(cell, str) and cell in 'xABC':
                block_type = 'gray'
            elif hasattr(cell, '__class__'):
                block_type = type(cell).__name__

            color = COLOR_MAP.get(block_type, 'white')
            draw.rectangle([top_left, bottom_right], fill=color, outline='black')

    # Draw lazor paths
    if lazors:
        for path in lazors:
            if len(path) < 2:
                continue
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]

                px1 = MARGIN + x1 * CELL_SIZE / 2
                py1 = MARGIN + y1 * CELL_SIZE / 2
                px2 = MARGIN + x2 * CELL_SIZE / 2
                py2 = MARGIN + y2 * CELL_SIZE / 2

                draw.line((px1, py1, px2, py2), fill="red", width=2)

    image.save(filename)
from matplotlib import pyplot as plt
import matplotlib.patches as patches

def draw_board_with_targets(grid, block_positions, lazor_paths, targets, filename='board.png'):
    """
    Draws the board with lazor paths and target points.
    """
    height = len(grid)
    width = len(grid[0])

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xticks(range(width + 1))
    ax.set_yticks(range(height + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)

    block_colors = {
        'ReflectBlock': 'blue',
        'OpaqueBlock': 'black',
        'RefractBlock': 'green'
    }

    for (x, y, block_type) in block_positions:
        color = block_colors.get(block_type, 'gray')
        rect = patches.Rectangle((x, height - y - 1), 1, 1, facecolor=color)
        ax.add_patch(rect)

    for path in lazor_paths:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            ax.plot([x1 / 2, x2 / 2], [height - y1 / 2, height - y2 / 2], 'r')

    for (tx, ty) in targets:
        ax.plot(tx / 2, height - ty / 2, 'o', color='orange', markersize=6)

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    plt.axis('off')
    output_path = f"/mnt/data/{filename}"
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    output_path
