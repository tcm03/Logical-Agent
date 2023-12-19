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
    for row in range(size):
        for col in range(size):
            if 'W' in world_map[row][col]:
                update_adjacent(world_map, row, col, 'S')
            if 'P' in world_map[row][col]:
                update_adjacent(world_map, row, col, 'B')


def update_adjacent(world_map, row, col, perception):
    size = len(world_map)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < size and 0 <= new_col < size:
            if world_map[new_row][new_col] == '-':
                world_map[new_row][new_col] = perception
            else:
                world_map[new_row][new_col] = ",".join([world_map[new_row][new_col], perception])

# Example:
# file_path = "test_input.txt" # Replace with the actual file path
# input_map = read_map(file_path)
# infer_information(input_map)