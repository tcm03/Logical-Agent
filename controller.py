import random
import numpy as np

"""

HOW TO USE?

# Generate a random map of any size between 2x2 and 10x10
gameController = GameController()

# Load map from file
gameController = GameController('C:/Users/ABC/map1.txt')

# [stench, breeze, glitter, bump, scream], where each field is a boolean
gameController.perceive()

# To go left, return True if the action is valid, False otherwise, None if the game is finished
gameController.act('left') 

# To go right, return True if the action is valid, False otherwise, None if the game is finished
gameController.act('right')

# To go forward, return True if the action is valid, False otherwise, None if the game is finished
gameController.act('forward')

# To grab gold, return True if the action is valid, False otherwise, None if the game is finished
gameController.act('grab')

# To shoot in the current direction, return True if the action is valid, False otherwise, None if the game is finished
gameController.act('shoot')

# To climb out of the map if the agent is at the bottom-left corner
gameController.act('climb')

Note: When the game is finished (gameController.finish == True), calls to gameController.act() and gameController.perceive() will return None.

These getters and methods are for reference only, do not use them to make decisions while playing game:

gameController.position # Current position of the agent (0-based)
gameController.direction # Current direction of the agent ('L', 'R', 'U', 'D')
gameController.score # Current score of the agent
gameController.finish # True if the game is finished, False otherwise
gameController.view_map() # View map

"""

class GameState():
    def __init__(self, size, position, direction, has_wumpus, has_pit, has_gold):
        self.size = size
        self.position = position
        self.direction = direction
        self.game_finished = False
        self.has_bump = False
        self.has_scream = False
        self.score = 0
        self.has_wumpus = has_wumpus
        self.has_pit = has_pit
        self.has_gold = has_gold

class GameController():
    
    def __init__(self, file_path = None):
        if file_path:
            self.__load_from_file(file_path)
        else: self.__generate()
    
    @property
    def position(self):
        return self.__state.position
    
    @property
    def direction(self):
        return self.__state.direction
    
    @property
    def score(self):
        return self.__state.score

    @property
    def finish(self):
        return self.__state.game_finished
    
    def perceive(self):
        if self.__state.game_finished:
            return None
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        has_stench = False
        has_breeze = False
        for x_offset, y_offset in movements:
            x = self.__state.position[0] + x_offset
            y = self.__state.position[1] + y_offset
            if x >= 0 and x < self.__state.size and y >= 0 and y < self.__state.size:
                if self.__state.has_wumpus[x, y]:
                    has_stench = True
                if self.__state.has_pit[x, y]:
                    has_breeze = True
        return has_stench, has_breeze, self.__state.has_gold[self.__state.position[0], self.__state.position[1]], self.__state.has_bump, self.__state.has_scream

    def act(self, action):
        if self.__state.game_finished:
            return None
        self.__state.has_bump = False
        self.__state.has_scream = False
        if action == 'left':
            self.__turn_left()
            return True
        elif action == 'right':
            self.__turn_right()
            return True
        elif action == 'forward':
            self.__go_forward()
            return True
        elif action == 'grab':
            if self.__state.has_gold[self.__state.position[0], self.__state.position[1]]:
                self.__state.has_gold[self.__state.position[0], self.__state.position[1]] = False
                self.__state.score += 1000
            return True
        elif action == 'shoot':
            self.__shoot()
            return True
        elif action == 'climb':
            if self.__state.position == [self.__state.size-1, 0]:
                self.__state.game_finished = True
                self.__state.score += 10
            return True
        else: return False
    
    def view_map(self):
        print(self.__state.has_wumpus)
        print(self.__state.has_pit)
        print(self.__state.has_gold)
        map_matrix = [['-' for _ in range(self.__state.size)] for _ in range(self.__state.size)]
        
        for i in range(self.__state.size):
            for j in range(self.__state.size):
                if self.__state.position == [i, j]:
                    map_matrix[i][j] += 'A'
                if self.__state.has_wumpus[i][j]:
                    map_matrix[i][j] += 'W'
                if self.__state.has_pit[i][j]:
                    map_matrix[i][j] += 'P'
                if self.__state.has_gold[i][j]:
                    map_matrix[i][j] += 'G'
        
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for i in range(self.__state.size):
            for j in range(self.__state.size):
                if map_matrix[i][j] != '-W' and map_matrix[i][j] != '-P':
                    for x_offset, y_offset in movements:
                        x = i + x_offset
                        y = j + y_offset
                        if x >= 0 and x < self.__state.size and y >= 0 and y < self.__state.size:
                            if 'W' in map_matrix[x][y] and 'S' not in map_matrix[i][j]:
                                map_matrix[i][j] += 'S'
                            elif 'P' in map_matrix[x][y] and 'B' not in map_matrix[i][j]:
                                map_matrix[i][j] += 'B'
        
        for i in range(self.__state.size):
            for j in range(self.__state.size):
                if len(map_matrix[i][j]) > 1:
                    assert map_matrix[i][j][0] == '-', "Invalid map matrix"
                    map_matrix[i][j] = map_matrix[i][j][1:]
        
        for row in map_matrix:
            print('.'.join(row))
    
    def __load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            size = int(lines[0])
            map_data = [line.strip() for line in lines[1:]]

            has_wumpus = np.zeros((size, size), dtype=bool)
            has_pit = np.zeros((size, size), dtype=bool)
            has_gold = np.zeros((size, size), dtype=bool)
            position = [0, 0]
            
            for i in range(size):
                rooms = map_data[i].split('.')
                for j in range(size):
                    room = rooms[j]
                    if room == 'W':
                        has_wumpus[i][j] = True
                    elif room == 'P':
                        has_pit[i][j] = True
                    elif room == 'G':
                        has_gold[i][j] = True
                    elif room == 'A':
                        position = (i, j)
            
            self.__state = GameState(
                size = size,
                position = position,
                direction = 'R',
                has_wumpus = has_wumpus,
                has_pit = has_pit,
                has_gold = has_gold
            )

    def __generate(self):
        size = random.randint(2, 10)
        position = [random.randint(0, size-1), random.randint(0, size-1)]

        num_remaining_cells = size * size - 1
        num_golds = random.randint(1, num_remaining_cells-2)
        num_wumpuses = random.randint(1, num_remaining_cells - num_golds - 1)
        num_pits = random.randint(1, num_remaining_cells - num_golds - num_wumpuses)
        has_wumpus = np.zeros((size, size), dtype=bool)
        has_pit = np.zeros((size, size), dtype=bool)
        has_gold = np.zeros((size, size), dtype=bool)
        remaining_cells = [(i, j) for i in range(size) for j in range(size) if (i, j) != (position[0], position[1])]

        for _ in range(num_golds):
            pos = random.choice(remaining_cells)
            has_gold[pos] = True
            remaining_cells.remove(pos)
        for _ in range(num_wumpuses):
            pos = random.choice(remaining_cells)
            has_wumpus[pos] = True
            remaining_cells.remove(pos)
        for _ in range(num_pits):
            pos = random.choice(remaining_cells)
            has_pit[pos] = True
            remaining_cells.remove(pos)

        self.__state = GameState(
            size = size,
            position = position,
            direction = 'R',
            has_wumpus = has_wumpus,
            has_pit = has_pit,
            has_gold = has_gold
        )
          
                
    def __turn_left(self):
        if self.__state.direction == 'R':
            self.__state.direction = 'U'
        elif self.__state.direction == 'U':
            self.__state.direction = 'L'
        elif self.__state.direction == 'L':
            self.__state.direction = 'D'
        elif self.__state.direction == 'D':
            self.__state.direction = 'R'
        else:
            raise Exception('Invalid direction')
    
    def __turn_right(self):
        if self.__state.direction == 'R':
            self.__state.direction = 'D'
        elif self.__state.direction == 'D':
            self.__state.direction = 'L'
        elif self.__state.direction == 'L':
            self.__state.direction = 'U'
        elif self.__state.direction == 'U':
            self.__state.direction = 'R'
        else:
            raise Exception('Invalid direction')
    
    def __go_forward(self):
        if self.__state.direction == 'R':
            if self.__state.position[1] == self.__state.size - 1:
                self.__state.has_bump = True
                return
            self.__state.position[1] += 1
        elif self.__state.direction == 'D':
            if self.__state.position[0] == self.__state.size - 1:
                self.__state.has_bump = True
                return
            self.__state.position[0] += 1
        elif self.__state.direction == 'L':
            if self.__state.position[1] == 0:
                self.__state.has_bump = True
                return
            self.__state.position[1] -= 1
        elif self.__state.direction == 'U':
            if self.__state.position[0] == 0:
                self.__state.has_bump = True
                return
            self.__state.position[0] -= 1
        else:
            raise Exception('Invalid direction')
        self.__state.score -= 10
        if self.__state.has_wumpus[self.__state.position[0], self.__state.position[1]] or self.__state.has_pit[self.__state.position[0], self.__state.position[1]]:
            self.__state.game_finished = True
            self.__state.score -= 10000
    
    def __shoot(self):
        self.__state.score -= 100
        if self.__state.direction == 'R' and self.__state.position[1] < self.__state.size-1 and self.__state.has_wumpus[self.__state.position[0], self.__state.position[1]+1]:
            self.__state.has_wumpus[self.__state.position[0], self.__state.position[1]+1] = False
            self.__state.has_scream = True
        elif self.__state.direction == 'D' and self.__state.position[0] < self.__state.size-1 and self.__state.has_wumpus[self.__state.position[0]+1, self.__state.position[1]]:
            self.__state.has_wumpus[self.__state.position[0]+1, self.__state.position[1]] = False
            self.__state.has_scream = True
        elif self.__state.direction == 'L' and self.__state.position[1] > 0 and self.__state.has_wumpus[self.__state.position[0], self.__state.position[1]-1]:
            self.__state.has_wumpus[self.__state.position[0], self.__state.position[1]-1] = False
            self.__state.has_scream = True
        elif self.__state.direction == 'U' and self.__state.position[0] > 0 and self.__state.has_wumpus[self.__state.position[0]-1, self.__state.position[1]]:
            self.__state.has_wumpus[self.__state.position[0]-1, self.__state.position[1]] = False
            self.__state.has_scream = True