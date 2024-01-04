import random

def read_map(file_path):
    try:
        with open(file_path, 'r') as file:
            size = int(file.readline().strip())
            world_map = [file.readline().strip().split('.') for _ in range(size)]

        return world_map

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def infer_information(world_map):
    size = len(world_map)
    i, j = -1, -1
    for row in range(size):
        for col in range(size):
            if 'W' in world_map[row][col]:
                update_adjacent(world_map, row, col, 'S')
            if 'P' in world_map[row][col]:
                update_adjacent(world_map, row, col, 'B')
            if 'A' in world_map[row][col]:
                print("here1")
                if len(world_map[row][col]) == 1:
                    print("here2")
                    world_map[row][col] = '-'
                else:
                    print("here3")
                    world_map[row][col] = world_map[row][col].replace("A", "")
                i = row
                j = col
    return world_map, (i, j)

def update_adjacent(world_map, row, col, perception):
    size = len(world_map)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < size and 0 <= new_col < size:
            if world_map[new_row][new_col] == '-':
                world_map[new_row][new_col] = perception
            if perception in world_map[new_row][new_col]:
                continue
            else:
                world_map[new_row][new_col] = "".join([world_map[new_row][new_col], perception])

def generate_map(size):
    map = [["-" for i in range(size)] for i in range(size)]
    # generate at least
    player_x = random.randint(0, size - 1)
    player_y = random.randint(0, size - 1)
    map[player_y][player_x] = "P"

    x = random.randint(0, size - 1)
    y = random.randint(0, size - 1)
    while map[y][x] != "-":
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
    # print(f"y={y}, x={x}")
    map[y][x] = "G"

    while map[y][x] != "-":
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
    # print(f"y={y}, x={x}")
    map[y][x] = "W"

    for i in range(size):
        for j in range(size):
            if map[i][j] != "-":
                continue
            rand_num = random.random()  # Generate a random number between 0 and 1
            if rand_num < 0.6:  # 60% chance
                continue
            elif rand_num < 0.8:  # 20% chance
                room = "P"
            elif rand_num < 0.9:  # 10% chance
                room = "W"
            else:  # 10% chance
                room = "G"
            map[i][j] = room

    return map

map_game = read_map("test_input\\test_input7.txt")
world_map,_ = infer_information(map_game)
print(world_map)

# [['-', '-', 'G', '-', '-', '-', '-', 'B', 'P', 'B'], 
#  ['-', '-', '-', '-', '-', '-', '-', 'B', 'GB', 'S'], 
#  ['B', '-', 'G', 'B', '-', '-', 'B', 'PB', 'PBS', 'WB'], 
#  ['P', 'B', 'B', 'P', 'BS', 'B', 'P', 'B', 'B', 'S'], 
#  ['B', '-', '-', 'BS', 'WB', 'PS', 'GB', '-', 'G', '-'], 
#  ['PS', 'B', '-', '-', 'GS', 'B', '-', '-', 'B', '-'], 
#  ['WB', 'PS', 'B', '-', '-', '-', '-', 'B', 'PS', 'B'], 
#  ['PS', 'B', 'P', 'B', '-', '-', 'G', 'S', 'WBS', 'S'], 
#  ['B', '-', 'B', 'S', '-', '-', 'S', 'S', 'WS', 'S'], 
#  ['-', 'G', 'S', 'W', 'S', 'S', 'W', 'S', 'S', '-']]

# [['S', 'B', 'S', 'GB'], 
#  ['WB', 'PS', 'WB', 'PS'], 
#  ['S', 'B', 'S', 'B'], 
#  ['-', '-', '-', '-']]