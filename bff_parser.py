import re
def parse_bff(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    grid = []
    blocks = {"A": 0, "B": 0, "C": 0}
    lazors = []
    targets = []

    i = 0
    while i < len(lines):
        if lines[i] == "GRID START":
            i += 1
            while lines[i] != "GRID STOP":
                grid.append(lines[i].split())
                i += 1
        elif lines[i].startswith("A") or lines[i].startswith("B") or lines[i].startswith("C"):
            key, val = lines[i].split()
            blocks[key] = int(val)
        elif lines[i].startswith("L"):
            parts = list(map(int, lines[i].strip().split()[1:]))
            lazors.append({"position": (parts[0], parts[1]), "direction": (parts[2], parts[3])})


    

        elif lines[i].startswith("P"):
            match = re.search(r'\(([^)]+)\)', lines[i])
            if match:
                x, y = map(int, match.group(1).split(","))
                targets.append((x * 2, y * 2))

        i += 1

    return {"grid": grid, "blocks": blocks, "lazors": lazors, "targets": targets}


