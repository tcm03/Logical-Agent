# Following arrays are not consist with the map (just use for test)
from sprite import DIRECTION

import solver


# MOVEMENT_DEMO = [(3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (2, 2), (2, 1), (2, 0), (2, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 2), (1, 2), (1, 3), (0, 3), (0, 2), (0, 1), (0, 0), (0, 1), (0, 0), (1, 0), (0, 0), (1, 0), (2, 0), (3, 0)]
# SCORE_DEMO = [0, -10, -20, -30, -40, -50, -60, -70, -170, -180, -280, -290, -390, -400, -500, -510, 480, 470, 460, 450, 440, 430, 420, 410, 400, 390, 390]
#
# MOVE_LOG_DEMO = ['right', 'right', 'right', 'right', 'up', 'left', 'left', 'left', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'left', 'left', 'left', 'right', 'left', 'down', 'up', 'down', 'down', 'down']
#
# PERCEPT_DEMO = [["Stench", "Breeze"], [], ["Breeze"], ["Glitter"], ["Breeze"], ["Glitter"], [], ["Breeze"], ["Stench"],
#                 ["Stench", "Breeze"], [], ["Breeze"], ["Breeze"], ["Glitter"],["Stench", "Breeze"], [], ["Breeze"], ["Glitter"], ["Breeze"], ["Glitter"], [], ["Breeze"], ["Stench"],
#                 ["Stench", "Breeze"], [], ["Breeze"], ["Breeze"]]
#
#
# SHOOT_DEMO = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#
# GRAB_DEMO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#
# MAP_DEMO = [[['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['-',
# 'S', 'S', 'SG'], ['S', 'WS', 'WS', 'WS'], ['-', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['-', 'S', 'S', 'SG'], ['S', 'WS', 'WS', 'WS'], ['-', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['-', '-', 'S', 'SG'], ['-', 'S', 'WS', 'WS'], ['-', '-', 'S', 'S'], ['-', '-', '-', '-']], [['-', '-', 'S', 'SG'], ['-', 'S', 'WS', 'WS'], ['-', '-', 'S', 'S'], ['-', '-', '-', '-']], [['-', '-', '-',
# 'SG'], ['-', '-', 'S', 'W'], ['-', '-', '-', 'S'], ['-', '-', '-', '-']], [['-', '-', '-', 'SG'], ['-', '-', 'S', 'W'], ['-', '-', '-', 'S'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-',
# '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']]]
#
# DIRECTION_DEMO = ['right', 'right', 'right', 'right', 'up', 'left', 'left', 'left', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'left', 'left', 'left', 'right', 'left', 'down', 'up', 'down', 'down', 'down']
#

class SimpleController:
    def __init__(self):
        self.size = None
        self.step = 0
        self.path = None
        self.score = None
        self.shoot = None
        self.direction = None
        self.grab = None
        self.map = None
        self.len = None
        self.action = None
        
    def solver(self,filepath_map):
        path_list, point_list, shoot_list, direction_list, grab_list, map_list, action_list = solver.getParameter2(filepath_map)
        self.path = path_list
        self.score = point_list
        self.shoot = shoot_list
        self.direction = direction_list
        self.grab = grab_list
        self.map = map_list
        self.size = len(self.map[0])
        self.len = len(self.path)
        self.action = action_list
        
    def get_information(self):
        information = {}
        if self.step < self.len:
            information["score"] = self.get_score()
            information["map"] = self.get_map()

            information["position"] = self.get_movement()

            information["shoot"] = self.get_shoot()
            information["grab"] = self.get_grab()

            information["direction"] = self.get_direction()
            information["percept"] = self.get_percept()
            information["action"] = self.get_action()
            if information["shoot"][1]:
                information["percept"].append("Scream")
            self.step += 1
        return information

    def get_movement(self):
        if self.step < self.len:
            return self.path[self.step]
        return None

    def get_score(self):
        if self.step < self.len:
            return self.score[self.step]
        return None

    def get_shoot(self):
        if self.step < self.len:
            return self.shoot[self.step]
        return None

    def get_grab(self):
        if self.step < self.len:
            return self.grab[self.step]
        return None

    def get_map(self):
        if self.step < self.len:
            return self.map[self.step]
        return None

    def get_direction(self):
        if self.step < self.len:
            elem = self.direction[self.step]
            if elem == "right":
                return DIRECTION.RIGHT
            elif elem == "left":
                return DIRECTION.LEFT
            elif elem == "up":
                return DIRECTION.UP
            else:
                return DIRECTION.DOWN

        return None

    def get_action(self):
        if self.step < self.len:
            return self.action[self.step]
        return None

    def get_percept(self):
        current_map = self.get_map()
        pos = self.get_movement()
        current_room = current_map[pos[0]][pos[1]]
        percept = []
        if "B" in current_room:
            percept.append("Breeze")
        if "S" in current_room:
            percept.append("Stench")
        if "G" in current_room:
            percept.append("Glitter")
        return percept
