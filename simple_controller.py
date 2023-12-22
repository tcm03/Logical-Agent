
# Following arrays are not consist with the map (just use for test)

MOVEMENT_DEMO = [(0, 0), (0, 1), (0, 0), (1, 0), (1, 1), (1, 2), (1, 1), (2, 1), (2, 2), (2, 3), (2, 2), (3, 2), (3, 1),
                 (3, 0)]

SCORE_DEMO = [0, -10, -20, -30, -40, -50, -60, -70, -80, 910, 900, 1890, 1880, 1880]

MOVE_LOG_DEMO = ['right', 'right', 'left', 'down', 'right', 'right', 'left', 'down', 'right', 'right', 'left', 'down',
                 'left', 'left']

PERCEPT_DEMO = [["Stench", "Breeze"], [], ["Breeze"], ["Glitter"], ["Breeze"], ["Glitter"], [], ["Breeze"], ["Stench"],
                ["Stench", "Breeze"], [], ["Breeze"], ["Breeze"], ["Glitter"]]

SHOOT_DEMO = [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]

GRAB_DEMO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]

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
