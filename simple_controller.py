
# Following arrays are not consist with the map (just use for test)
from sprite import DIRECTION

MOVEMENT_DEMO = [(3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (2, 2), (2, 1), (2, 0), (2, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 2), (1, 2), (1, 3), (0, 3), (0, 2), (0, 1), (0, 0), (0, 1), (0, 0), (1, 0), (0, 0), (1, 0), (2, 0), (3, 0)]
SCORE_DEMO = [0, -10, -20, -30, -40, -50, -60, -70, -170, -180, -280, -290, -390, -400, -500, -510, 480, 470, 460, 450, 440, 430, 420, 410, 400, 390, 390]

MOVE_LOG_DEMO = ['right', 'right', 'right', 'right', 'up', 'left', 'left', 'left', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'left', 'left', 'left', 'right', 'left', 'down', 'up', 'down', 'down', 'down']

PERCEPT_DEMO = [["Stench", "Breeze"], [], ["Breeze"], ["Glitter"], ["Breeze"], ["Glitter"], [], ["Breeze"], ["Stench"],
                ["Stench", "Breeze"], [], ["Breeze"], ["Breeze"], ["Glitter"],["Stench", "Breeze"], [], ["Breeze"], ["Glitter"], ["Breeze"], ["Glitter"], [], ["Breeze"], ["Stench"],
                ["Stench", "Breeze"], [], ["Breeze"], ["Breeze"]]


SHOOT_DEMO = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

GRAB_DEMO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

MAP_DEMO = [[['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['S', 'S', 'S', 'SG'], ['WS', 'WS', 'WS', 'WS'], ['S', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['-', 
'S', 'S', 'SG'], ['S', 'WS', 'WS', 'WS'], ['-', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['-', 'S', 'S', 'SG'], ['S', 'WS', 'WS', 'WS'], ['-', 'S', 'S', 'S'], ['-', '-', '-', '-']], [['-', '-', 'S', 'SG'], ['-', 'S', 'WS', 'WS'], ['-', '-', 'S', 'S'], ['-', '-', '-', '-']], [['-', '-', 'S', 'SG'], ['-', 'S', 'WS', 'WS'], ['-', '-', 'S', 'S'], ['-', '-', '-', '-']], [['-', '-', '-', 
'SG'], ['-', '-', 'S', 'W'], ['-', '-', '-', 'S'], ['-', '-', '-', '-']], [['-', '-', '-', 'SG'], ['-', '-', 'S', 'W'], ['-', '-', '-', 'S'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', 
'-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']], [['-', '-', '-', 'G'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']]]

DIRECTION_DEMO = ['right', 'right', 'right', 'right', 'up', 'left', 'left', 'left', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'left', 'left', 'left', 'right', 'left', 'down', 'up', 'down', 'down', 'down']


class SimpleController:
    def __init__(self):
        self.step = 0

    def get_action(self):
        information = {}
        if self.step < len(MOVEMENT_DEMO):
            information["position"] = self.get_movement()
            information["score"] = self.get_score()
            information["log"] = self.get_log()
            information["percept"] = self.get_percept()
            information["shoot"] = self.get_shoot()
            information["grab"] = self.get_grab()
            information["map"] = self.get_map()
            information["direction"] = self.get_direction()
            self.step += 1
        return information

    def get_movement(self):
        if self.step < len(MOVEMENT_DEMO):
            return MOVEMENT_DEMO[self.step]
        return None

    def get_score(self):
        if self.step < len(SCORE_DEMO):
            return SCORE_DEMO[self.step]
        return None

    def get_log(self):
        if self.step < len(MOVE_LOG_DEMO):
            return MOVE_LOG_DEMO[self.step]
        return None

    def get_percept(self):
        if self.step < len(PERCEPT_DEMO):
            return PERCEPT_DEMO[self.step]
        return None

    def get_shoot(self):
        if self.step < len(SHOOT_DEMO):
            return SHOOT_DEMO[self.step]
        return None

    def get_grab(self):
        if self.step < len(GRAB_DEMO):
            return GRAB_DEMO[self.step]
        return None

    def get_map(self):
        if self.step < len(MAP_DEMO):
            return MAP_DEMO[self.step]
        return None

    def get_direction(self):
        if self.step < len(DIRECTION_DEMO):
            elem = DIRECTION_DEMO[self.step]
            if elem == "right":
                return DIRECTION.RIGHT
            elif elem == "left":
                return DIRECTION.LEFT
            elif elem == "up":
                return DIRECTION.UP
            else:
                return DIRECTION.DOWN

        return None