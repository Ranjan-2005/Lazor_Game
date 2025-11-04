from lazor_blocks import Block

class LazorSim:
    def __init__(self, grid, lazors, targets):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.lazors = lazors
        self.targets = set(targets)
        self.hit_targets = set()

    def simulate(self):
        self.hit_targets.clear()
        for lazor in self.lazors:
            self._trace(lazor["position"], lazor["direction"])
        return self.targets.issubset(self.hit_targets)

    def _trace(self, pos, direction, visited=None):
        if visited is None:
            visited = set()
        x, y = pos
        dx, dy = direction
        path = [(x, y)]

        for _ in range(200):
            x += dx
            y += dy
            path.append((x, y))

            if (x, y, dx, dy) in visited:
                break
            visited.add((x, y, dx, dy))

            if (x, y) in self.targets:
                self.hit_targets.add((x, y))

            if x < 0 or y < 0 or x > 2 * self.width or y > 2 * self.height:
                break

            # Check for block at center of a cell
            if x % 2 == 1 and y % 2 == 1:
                cx = (x - 1) // 2
                cy = (y - 1) // 2
                if 0 <= cx < self.width and 0 <= cy < self.height:
                    block = self.grid[cy][cx]
                    if isinstance(block, Block):
                        new_dirs = block.interact((x, y), (dx, dy))
                        if len(new_dirs) == 1:
                            dx, dy = new_dirs[0]  # continue straight
                        else:
                            # multiple beams (e.g., refracted + reflected)
                            split_paths = []
                            for new_dir in new_dirs:
                                split_paths += self._trace((x, y), new_dir, visited.copy())
                            return path + split_paths
        return path

    def get_paths(self):
        all_paths = []
        for lazor in self.lazors:
            path = self._trace(lazor["position"], lazor["direction"])
            all_paths.append(path)
        return all_paths
