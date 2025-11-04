import os
from lazor_solver import solve_bff          # returns (block_placements, lazor_paths) or None
from bff_parser import parse_bff            # returns dict with keys: 'grid', 'lasers', 'targets'
try:
    from visualize import draw_board_with_targets  # optional; may or may not accept out_png
    HAVE_VIZ = True
except Exception:
    HAVE_VIZ = False


def coerce_index_order(grid, a, b):
    """
    Given two integers (a, b) that might be (x,y) or (row,col),
    return a tuple (row, col) guaranteed in-bounds.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    # (a,b) as (row,col) valid?
    if 0 <= a < rows and 0 <= b < cols:
        return a, b
    # (a,b) as (x,y) -> (row=y, col=x) valid?
    if 0 <= b < rows and 0 <= a < cols:
        return b, a
    raise IndexError(f"Placement coordinate out of bounds: ({a},{b}) for grid {rows}x{cols}")


def build_solution_grid(grid, block_placements):
    """
    Return a deep-copied grid with solution blocks overlaid.
    block_placements items can be either:
      - (x, y, 'ReflectBlock'/'OpaqueBlock'/'RefractBlock')  OR
      - (row, col, 'A'/'B'/'C')
    """
    filled = [row[:] for row in grid]  # deep copy (list of lists)

    for *coords, block_type in block_placements:
        if len(coords) != 2:
            raise ValueError(f"Bad placement tuple (need 3 items): {coords + [block_type]}")
        a, b = coords

        # Map class names to letters if needed
        if block_type in ('ReflectBlock', 'OpaqueBlock', 'RefractBlock'):
            letter = {'ReflectBlock': 'A', 'OpaqueBlock': 'B', 'RefractBlock': 'C'}[block_type]
        elif block_type in ('A', 'B', 'C'):
            letter = block_type
        else:
            raise ValueError(f"Unknown block type: {block_type}")

        r, c = coerce_index_order(filled, a, b)
        filled[r][c] = letter

    return filled


def print_grid(grid):
    """Print the grid with tabs (works even if parser normalized spaces)."""
    for row in grid:
        print('\t'.join(row))
    print()


def save_solution_to_file(bff_path, block_placements, final_grid):
    """
    Writes a text file alongside the .bff:
      <name>_solution.txt
    Includes placements and the final grid (tab-separated).
    """
    base = os.path.splitext(bff_path)[0]
    out_txt = f"{base}_solution.txt"

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"Solution for {os.path.basename(bff_path)}\n")
        f.write("=" * 40 + "\n\n")
        f.write("Placements:\n")
        for *coords, block_type in block_placements:
            a, b = coords
            f.write(f"  {block_type} at ({a}, {b})\n")

        f.write("\nFinal grid:\n")
        for row in final_grid:
            f.write("\t".join(row) + "\n")

    print(f"Saved solution to {out_txt}")


def pretty_print_placements(block_placements):
    print("Placements:")
    for *coords, block_type in block_placements:
        a, b = coords
        print(f"  {block_type} at ({a}, {b})")


def solve_all_bff_in_folder(folder='.', visualize_png=False):
    any_found = False
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith('.bff'):
            continue
        path = os.path.join(folder, filename)
        print(f"Solving {filename}...")
        try:
            solution = solve_bff(path)   # pass the full path
            if solution:
                any_found = True
                block_placements, lazor_paths = solution
                parsed = parse_bff(path)  # full path again
                grid = parsed['grid']     # assumed list[list[str]]
                final_grid = build_solution_grid(grid, block_placements)

                pretty_print_placements(block_placements)
                print("solution grid:")
                print_grid(final_grid)

                # ---- NEW: write a .txt solution file next to the .bff
                save_solution_to_file(path, block_placements, final_grid)

                # Optional visualization if your function supports it
                if visualize_png and HAVE_VIZ:
                    try:
                        out_png = os.path.splitext(path)[0] + "_solution.png"
                        # Some visualize modules don't accept out_png; the try/except keeps us safe.
                        draw_board_with_targets(final_grid, lazor_paths, parsed.get('targets', set()), out_png=out_png)
                        print(f"Wrote {out_png}")
                    except TypeError:
                        # Fall back to a no-kw-call if signature is (grid, paths, targets)
                        try:
                            draw_board_with_targets(final_grid, lazor_paths, parsed.get('targets', set()))
                            print("(visualize) drew image (no save path supported by visualize.py)")
                        except Exception as viz_e2:
                            print(f"(visualize) skipped: {viz_e2}")
                    except Exception as viz_e:
                        print(f"(visualize) skipped: {viz_e}")
            else:
                print(f"No solution found for {filename}")
        except Exception as e:
            print(f"Failed to solve {filename}: {e}")
    if not any_found:
        print("No .bff files solved.")


if __name__ == '__main__':
    # Change folder if your .bff files live elsewhere, e.g. 'Lazor Project/boards'
    solve_all_bff_in_folder(folder='.', visualize_png=True)
