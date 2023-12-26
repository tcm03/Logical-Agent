
# Following arrays are not consist with the map (just use for test)
from sprite import DIRECTION

MOVEMENT_DEMO = [(0, 0), (0, 1), (0, 1), (0, 2), (0, 3), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (1, 0), (2, 0), (3, 0), (3, 0)]

SCORE_DEMO = [0, -100, -110, -120, -220, 770, 760, 750, 740, 640, 630, 620, 520, 520]

MOVE_LOG_DEMO = ['right', 'right', 'right', 'right', 'right', 'right', 'left', 'left', 'left', 'down', 'down', 'down', 'down', 'down']

PERCEPT_DEMO = [["Stench", "Breeze"], [], ["Breeze"], ["Glitter"], ["Breeze"], ["Glitter"], [], ["Breeze"], ["Stench"],
                ["Stench", "Breeze"], [], ["Breeze"], ["Breeze"], ["Glitter"]]

SHOOT_DEMO = [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]

GRAB_DEMO = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]

MAP_DEMO =
DIRECTION_DEMO = ['right', 'right', 'left', 'down', 'right', 'right', 'left', 'down', 'right', 'right', 'left', 'down', 'left', 'left']


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