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
                if len(world_map[row][col]) == 1:
                    world_map[row][col] = '-'
                    i = row
                    j = col
                else:
                    world_map[row][col].replace("A", "")
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
    for i in range(size):
        for j in range(size):
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


