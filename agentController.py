
import random
import copy
from queue import PriorityQueue
import numpy as np


class AgentController:
    def __init__(self,N,map_game,try_stop):
        self.map_game = map_game
        self.currentCave = None
        self.direction = "right"
        self.P = [] 
        self.G = []
        self.W = []
        self.visited = []
        self.size = N
        self.knowledgePit = []
        self.knowledgeWum = []
        self.path = []
        self.point = [0]
        self.shoot = []
        self.try_stop = try_stop
        self.direction_list=[]
        self.grab = []
        self.map_list = []
        self.end = None
        
        
        for _ in range(N):
            temp = []
            for _ in range(N):
                temp.append("-1")
            self.P.append(temp)
            
        for _ in range(N):
            temp = []
            for _ in range(N):
                temp.append("-1")
            self.G.append(temp)
            
        for _ in range(N):
            temp = []
            for _ in range(N):
                temp.append("-1")
            self.W.append(temp)
            
        for _ in range(N):
            temp = []
            for _ in range(N):
                temp.append("-1")
            self.visited.append(temp)
    
        
    
    
    def perceive(self):
        moves = [(0, 1), (-1, 0), (0, -1),(1, 0)]
        
        x, y = self.currentCave
        
        if self.map_game[x][y] == "-" or self.map_game[x][y] == "G":
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset

                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                    continue
                
                self.updatePit(next_x,next_y,"0")
                for i in range(len(self.knowledgePit)):
                    if self.knowledgePit[i] == "":
                        continue
                    if f"{next_x},{next_y}?" in self.knowledgePit[i]:
                        self.knowledgePit[i] = self.knowledgePit[i].replace(f"{next_x},{next_y}?","")
                        
                    temp = self.knowledgePit[i].split("?")
                    if len(temp) == 2:
                        temp1 = temp[0].split(",")
                        self.updatePit(int(temp1[0]),int(temp1[1]),"1")
                        self.knowledgePit[i] = ""
                        
                self.updateWumPus(next_x,next_y,"0")
                for i in range(len(self.knowledgeWum)):
                    if self.knowledgeWum[i] == "":
                        continue
                    if f"{next_x},{next_y}?" in self.knowledgeWum[i]:
                        self.knowledgeWum[i] = self.knowledgeWum[i].replace(f"{next_x},{next_y}?","")
                        
                    temp = self.knowledgeWum[i].split("?")
                    if len(temp) == 2:
                        temp1 = temp[0].split(",")
                        self.updateWumPus(int(temp1[0]),int(temp1[1]),"1")
                        self.knowledgeWum[i] = ""
        
        
        
        if "B" in self.map_game[x][y]:
            createLogicPit = []
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset
                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                    continue
                if self.confirmPit(next_x,next_y) == "-1":
                    createLogicPit.append((next_x,next_y,-1))
                if self.confirmPit(next_x,next_y) == "1":
                    createLogicPit.append((next_x,next_y,1))
            if len(createLogicPit) == 1:
                if createLogicPit[0][2] == -1:
                    self.updatePit(createLogicPit[0][0],createLogicPit[0][1],"1")
            else:
                string_logic = ""
                for cave in createLogicPit:
                    string_logic += f"{cave[0]},{cave[1]}?"
                self.knowledgePit.append(string_logic)
        if "S" in self.map_game[x][y]:
            createLogicWum = []
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset
                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                    continue
                if self.confirmWumpus(next_x,next_y) == "-1":
                    createLogicWum.append((next_x,next_y,-1))
                if self.confirmWumpus(next_x,next_y) == "1":
                    createLogicWum.append((next_x,next_y,1))
                if len(createLogicWum) == 1:
                    if createLogicWum[0][2] == -1:
                        self.updateWumPus(createLogicWum[0][0],createLogicWum[0][1],"1")
                else:
                    string_logic = ""
                    for cave in createLogicWum:
                        string_logic += f"{cave[0]},{cave[1]}?"
                    self.knowledgeWum.append(string_logic)
        if "S" not in self.map_game[x][y]:
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset
                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                    continue
                self.updateWumPus(next_x,next_y,"0")
                for i in range(len(self.knowledgeWum)):
                    if self.knowledgeWum[i] == "":
                        continue
                    if f"{next_x},{next_y}?" in self.knowledgeWum[i]:
                        self.knowledgeWum[i] = self.knowledgeWum[i].replace(f"{next_x},{next_y}?","")
                    temp = self.knowledgeWum[i].split("?")
                    if len(temp) == 2:
                        temp1 = temp[0].split(",")
                        self.updateWumPus(int(temp1[0]),int(temp1[1]),"1")
                        self.knowledgeWum[i] = ""
        if "B" not in self.map_game[x][y]:
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset
                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                    continue
                self.updatePit(next_x,next_y,"0")
                for i in range(len(self.knowledgePit)):
                    if self.knowledgePit[i] == "":
                        continue
                    if f"{next_x},{next_y}?" in self.knowledgePit[i]:
                        self.knowledgePit[i] = self.knowledgePit[i].replace(f"{next_x},{next_y}?","")
                    temp = self.knowledgePit[i].split("?")
                    if len(temp) == 2:
                        temp1 = temp[0].split(",")
                        self.updatePit(int(temp1[0]),int(temp1[1]),"1")
                        self.knowledgePit[i] = ""
                        
    def confirmPit(self,x,y):
        return self.P[x][y]
    
    def confirmWumpus(self,x,y):
        return self.W[x][y]
        
    
    def updateAfterGold(self):
        x, y = self.currentCave
        if "G" in self.map_game[x][y]:
            txt = self.map_game[x][y]
            temp = txt[0:txt.index("G")]+txt[txt.index("G")+1:]
            self.map_game[x][y]=temp
            if self.map_game[x][y] == "":
                self.map_game[x][y]='-'
    
    
    
    def confirmScream(self):
        if self.direction == "left":
            i = self.currentCave[1]-1
            if i < 0 or i>=self.size:
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                return False
            if "W" in self.map_game[self.currentCave[0]][i]:
                self.updateWumPus(self.currentCave[0],self.currentCave[1]-1,"1")
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                txt = self.map_game[self.currentCave[0]][i]
                temp = txt[0:txt.index("W")]+txt[txt.index("W")+1:]
                self.map_game[self.currentCave[0]][i]=temp
                if self.map_game[self.currentCave[0]][i] == "":
                    self.map_game[self.currentCave[0]][i]='-'
                return True
            else:
                self.updateWumPus(self.currentCave[0],self.currentCave[1]-1,"0")
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                return False
        if self.direction == "right":
            i = self.currentCave[1]+1
            if i < 0 or i>=self.size:
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                return False
            if "W" in self.map_game[self.currentCave[0]][i]:
                self.updateWumPus(self.currentCave[0],self.currentCave[1]+1,"1")
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                txt = self.map_game[self.currentCave[0]][i]
                temp = txt[0:txt.index("W")]+txt[txt.index("W")+1:]
                self.map_game[self.currentCave[0]][i]=temp
                if self.map_game[self.currentCave[0]][i] == "":
                    self.map_game[self.currentCave[0]][i]='-'
                return True
            else:
                self.updateWumPus(self.currentCave[0],self.currentCave[1]+1,"0")
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                return False
        if self.direction == "up":
            i = self.currentCave[0]-1
            if i < 0 or i>=self.size:
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                return False
            if "W" in self.map_game[i][self.currentCave[1]]:
                self.updateWumPus(self.currentCave[0]-1,self.currentCave[1],"1")
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                txt = self.map_game[i][self.currentCave[1]]
                temp = txt[0:txt.index("W")]+txt[txt.index("W")+1:]
                self.map_game[i][self.currentCave[1]]=temp
                if self.map_game[i][self.currentCave[1]] == "":
                    self.map_game[i][self.currentCave[1]]='-'
                return True
            else:
                self.updateWumPus(self.currentCave[0]-1,self.currentCave[1],"0")
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                return False
        if self.direction == "down":
            i = self.currentCave[0]+1
            if i < 0 or i>=self.size:
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                return False
            if "W" in self.map_game[i][self.currentCave[1]]:
                self.updateWumPus(self.currentCave[0]+1,self.currentCave[1],"1")
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                txt = self.map_game[i][self.currentCave[1]]
                temp = txt[0:txt.index("W")]+txt[txt.index("W")+1:]
                self.map_game[i][self.currentCave[1]]=temp
                if self.map_game[i][self.currentCave[1]] == "":
                    self.map_game[i][self.currentCave[1]]='-'
                return True
            else:
                self.updateWumPus(self.currentCave[0]+1,self.currentCave[1],"0")
                self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                return False
            
    def updateMap(self):
        moves = [(0,1),(0,-1),(1,0),(-1,0)]
        for i in range(self.size):
            for j in range(self.size):
                if "S" in self.map_game[i][j]:
                    dem = 0
                    for x_offset, y_offset in moves:
                        next_x, next_y = i + x_offset, j + y_offset
                        if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                            continue
                        if "W" in self.map_game[next_x][next_y]:
                            if "S" not in self.map_game[i][j]:
                                if self.map_game[i][j] == "-":
                                    self.map_game[i][j] = "S"
                                else:
                                    self.map_game[i][j] = self.map_game[i][j] + "S"
                            dem+=1
                            break
                    if dem == 0:
                        txt = self.map_game[i][j]
                        temp = txt[0:txt.index("S")]+txt[txt.index("S")+1:]
                        self.map_game[i][j]=temp
                        if self.map_game[i][j] == "":
                            self.map_game[i][j]='-'
        for i in range(self.size):
            for j in range(self.size):
                for x_offset, y_offset in moves:
                        next_x, next_y = i + x_offset, j + y_offset
                        if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                            continue
                        if "P" in self.map_game[next_x][next_y]:
                            if "B" not in self.map_game[i][j]:
                                if self.map_game[i][j] == "-":
                                    self.map_game[i][j] = "B"
                                else:
                                    self.map_game[i][j] = self.map_game[i][j] + "B"
                            break

    def updatePit(self, x, y, check):
        self.P[x][y] = check

    def updateWumPus(self, x, y, check):
        self.W[x][y] = check
    
    def updateGold(self, x, y, check):
        if "G" in self.map_game[x][y]:
            self.G[x][y] = check
    
    def updateCurrentState(self,x,y):
        self.currentCave = {x,y}
    
    def updatePerceiveAgent(self,start,map_game,old,check_style,direction):
        self.currentCave = start
        if start == (self.size-1,0):
            self.end = start
        self.map_game = map_game
        if old == (-1,-1):
            self.P[start[0]][start[1]] = "0"
            self.W[start[0]][start[1]] = "0"
        temp_point = self.point[-1]
        self.direction = direction
        if check_style == 1:
            temp_point -= 100
            self.currentCave = self.path[-1]
            # self.path.append(start)
            self.path.append(old)
            self.direction_list.append(direction)
            self.point.append(temp_point)
            temp_map = copy.deepcopy(self.map_game)
            is_scream = self.confirmScream()
            # self.map_list.append(temp_map)
            if is_scream == True:
                self.updateMap()
                temp_map = copy.deepcopy(self.map_game)
                self.shoot.append((1,1))
            else:
                self.shoot.append((1,0))
            self.map_list.append(temp_map)
            self.map_list.append(temp_map)
            self.currentCave= start
            if "G" in self.map_game[start[0]][start[1]] and self.G[start[0]][start[1]] != "1":
                self.grab.append(0)
                self.grab.append(1)
            if "G" not in self.map_game[start[0]][start[1]] or self.G[start[0]][start[1]] == "1":
                self.grab.append(0)
                self.grab.append(0)
        if check_style != 1:
            if "G" in self.map_game[start[0]][start[1]] and self.G[start[0]][start[1]] != "1":
                self.grab.append(1)
            if "G" not in self.map_game[start[0]][start[1]] or self.G[start[0]][start[1]] == "1":
                self.grab.append(0)
        self.perceive()
        self.visited[start[0]][start[1]] = "1"
        self.path.append(start)
        if check_style != 1:
            self.map_list.append(copy.deepcopy(self.map_game))
        self.shoot.append((0,0))
        self.direction_list.append(direction)
        if old != (-1,-1):
            if "P" in self.map_game[start[0]][start[1]]:
                temp_point -= 10000
            if "G" in self.map_game[start[0]][start[1]] and self.G[start[0]][start[1]] != "1":
                temp_point += 1000
                self.G[start[0]][start[1]] = "1"
            if "W" in self.map_game[start[0]][start[1]] and self.W[start[0]][start[1]]=="1" and check_style!=1:
                temp_point -= 10000
            temp_point -= 10
            self.point.append(temp_point)
    def checkAgentDie(self,start,check_style):
        return "P" in self.map_game[start[0]][start[1]] or ("W" in self.map_game[start[0]][start[1]] and self.W[start[0]][start[1]]=="1" and check_style != 1)
    
    def getReturnParameter(self):
        return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list,"Stop"
    
    def find_path_to_exit(self, start, end):
        print("Startexit:, ",start)
        path_save = None
        shoot_list_save = None
        direction_list_save = None 
        map_list_save = None
        trace = []
        visited = []
        for _ in range(self.size):
            temp = []
            temp_visited = []
            for _ in range(self.size):
                temp.append(((-1,-1),0))
                temp_visited.append(0)
            trace.append(temp)
            visited.append(temp_visited)
        old_map = copy.deepcopy(self.map_game)
        old_knowPit =copy.deepcopy(self.knowledgePit)
        old_knowWum = copy.deepcopy(self.knowledgeWum)
        old_p = copy.deepcopy(self.P)
        old_w = copy.deepcopy(self.W)
        old_g = copy.deepcopy(self.G)
        old_direction = copy.deepcopy(self.direction)
        old_map1 = copy.deepcopy(self.map_game)
        old_knowPit1 =copy.deepcopy(self.knowledgePit)
        old_knowWum1 = copy.deepcopy(self.knowledgeWum)
        old_p1 = copy.deepcopy(self.P)
        old_w1 = copy.deepcopy(self.W)
        old_g1 = copy.deepcopy(self.G)
        old_direction1 = copy.deepcopy(self.direction)
        frontier = PriorityQueue()
        frontier.put([0, start,(-1,-1),old_direction1,0,old_map1,old_knowPit1,old_knowWum1,old_p1,old_w1,old_g1])
        self.updatePit(start[0],start[1],"0")
        self.updateWumPus(start[0],start[1],"0")
        moves = [(-1, 0), (0, 1), (0, -1),(1, 0)]
        while frontier.qsize() != 0:
            cost, position ,old_position, direction,is_shoot,old_map2,old_knowPit2,old_knowWum2,old_p2,old_w2,old_g2 = frontier.get()
            self.currentCave = position
            self.map_game=copy.deepcopy(old_map2)
            self.knowledgePit=copy.deepcopy(old_knowPit2)
            self.knowledgeWum=copy.deepcopy(old_knowWum2)
            self.P=copy.deepcopy(old_p2)
            self.W=copy.deepcopy(old_w2)
            self.G=copy.deepcopy(old_g2)
            self.direction= direction
            self.currentCave = old_position
            kiemtra = False
            if is_shoot == 1:
                kiemtra = self.confirmScream()
                if kiemtra:
                    self.updateMap()
            self.currentCave = position
            print(position)
            print(self.P)
            self.perceive()
            print(self.P)
            x, y = position
            if visited[x][y]:
                continue
            visited[x][y] = 1
            trace[x][y] = (old_position,is_shoot,direction,copy.deepcopy(old_map2),kiemtra)
            
            temp_current_start = None
            temp_current_map_game = None
            temp_current_knowP = None
            temp_current_knowW = None
            temp_current_P = None
            temp_current_W = None
            temp_current_G = None
            temp_current_direction = None
            if frontier.qsize() == 0:
                temp_current_start = copy.deepcopy(self.currentCave)
                temp_current_map_game = copy.deepcopy(self.map_game)
                temp_current_knowP = copy.deepcopy(self.knowledgePit)
                temp_current_knowW = copy.deepcopy(self.knowledgeWum)
                temp_current_P = copy.deepcopy(self.P)
                temp_current_W = copy.deepcopy(self.W)
                temp_current_G = copy.deepcopy(self.G)
                temp_current_direction = copy.deepcopy(self.direction)
            
            if frontier.qsize() == 0:
                self.currentCave = start
                temp_check_map = copy.deepcopy(self.map_game)
                self.map_game=copy.deepcopy(old_map)
                self.knowledgePit=copy.deepcopy(old_knowPit)
                self.knowledgeWum=copy.deepcopy(old_knowWum)
                self.P=copy.deepcopy(old_p)
                self.W=copy.deepcopy(old_w)
                self.G=copy.deepcopy(old_g)
                self.direction= copy.deepcopy(old_direction)
                path = []
                shoot_list = [(0,0)]
                direction_list = []
                check_sort = is_shoot
                map_list = []
                while position != start: 
                    if check_sort == 1:
                        path.append(position)
                        # path.append(position)
                        if kiemtra:
                            shoot_list.append((1,1))
                        else:
                            shoot_list.append((1,0))
                        map_list.append(temp_check_map)
                        shoot_list.append((0,0))
                        # map_list.append(trace[position[0]][position[1]][3])
                        map_list.append(temp_check_map)
                        temp_check_map = trace[position[0]][position[1]][3]
                        direction_list.append(trace[position[0]][position[1]][2])
                        direction_list.append(trace[position[0]][position[1]][2])
                        position = trace[position[0]][position[1]][0]
                        path.append(position)
                        check_sort = trace[position[0]][position[1]][1]
                        kiemtra = trace[position[0]][position[1]][4]
                    else:
                        path.append(position)
                        shoot_list.append((0,0))
                        direction_list.append(trace[position[0]][position[1]][2])
                        map_list.append(trace[position[0]][position[1]][3])
                        temp_check_map = trace[position[0]][position[1]][3]
                        position = trace[position[0]][position[1]][0]
                        check_sort = trace[position[0]][position[1]][1]
                        kiemtra = trace[position[0]][position[1]][4]
                path.append(start)
                path.reverse()
                shoot_list.reverse()
                direction_list.reverse()
                map_list.reverse()
                self.currentCave = start
                self.map_game=copy.deepcopy(old_map)
                self.knowledgePit=copy.deepcopy(old_knowPit)
                self.knowledgeWum=copy.deepcopy(old_knowWum)
                self.P=copy.deepcopy(old_p)
                self.W=copy.deepcopy(old_w)
                self.G=copy.deepcopy(old_g)
                self.direction= old_direction
                path_save = copy.deepcopy(path)
                shoot_list_save = copy.deepcopy(shoot_list)
                direction_list_save = copy.deepcopy(direction_list)
                map_list_save = copy.deepcopy(map_list)
                
            
            if frontier.qsize() == 0:
                self.currentCave = temp_current_start
                self.map_game = temp_current_map_game
                self.knowledgePit = temp_current_knowP
                self.knowledgeWum = temp_current_knowW
                self.P = temp_current_P
                self.W = temp_current_W
                self.G = temp_current_G
                self.direction = temp_current_direction
                
            
            
            if self.map_game[x][y] == "P" or ("W" in self.map_game[x][y] and is_shoot == 0):
                self.currentCave = start
                temp_check_map = copy.deepcopy(self.map_game)
                self.map_game=copy.deepcopy(old_map)
                self.knowledgePit=copy.deepcopy(old_knowPit)
                self.knowledgeWum=copy.deepcopy(old_knowWum)
                self.P=copy.deepcopy(old_p)
                self.W=copy.deepcopy(old_w)
                self.G=copy.deepcopy(old_g)
                self.direction= old_direction
                path = []
                shoot_list = [(0,0)]
                direction_list = []
                check_sort = is_shoot
                map_list = []
                
                while position != start:
                    if check_sort == 1:
                        path.append(position)
                        # path.append(position)
                        if kiemtra:
                            shoot_list.append((1,1))
                        else:
                            shoot_list.append((1,0))
                        map_list.append(temp_check_map)
                        shoot_list.append((0,0))
                        # map_list.append(trace[position[0]][position[1]][3])
                        map_list.append(temp_check_map)
                        temp_check_map = copy.deepcopy(trace[position[0]][position[1]][3])
                        direction_list.append(trace[position[0]][position[1]][2])
                        direction_list.append(trace[position[0]][position[1]][2])
                        position = trace[position[0]][position[1]][0]
                        path.append(position)
                        check_sort = trace[position[0]][position[1]][1]
                        kiemtra = trace[position[0]][position[1]][4]
                    else:
                        path.append(position)
                        shoot_list.append((0,0))
                        direction_list.append(trace[position[0]][position[1]][2])
                        map_list.append(trace[position[0]][position[1]][3])
                        temp_check_map = copy.deepcopy(trace[position[0]][position[1]][3])
                        position = trace[position[0]][position[1]][0]
                        check_sort = trace[position[0]][position[1]][1]
                        kiemtra = trace[position[0]][position[1]][4]
                path.append(start)  
                path.reverse()  
                shoot_list.reverse()
                direction_list.reverse()
                map_list.reverse()
                return path,shoot_list,direction_list,map_list, False
            
            if position == end:
                self.currentCave = start
                temp_check_map = copy.deepcopy(self.map_game)
                self.map_game=copy.deepcopy(old_map)
                self.knowledgePit=copy.deepcopy(old_knowPit)
                self.knowledgeWum=copy.deepcopy(old_knowWum)
                self.P=copy.deepcopy(old_p)
                self.W=copy.deepcopy(old_w)
                self.G=copy.deepcopy(old_g)
                self.direction= copy.deepcopy(old_direction)
                path = []
                shoot_list = [(0,0)]
                direction_list = []
                check_sort = is_shoot
                map_list = []
                while position != start: 
                    if check_sort == 1:
                        path.append(position)
                        # path.append(position)
                        if kiemtra:
                            shoot_list.append((1,1))
                        else:
                            shoot_list.append((1,0))
                        map_list.append(temp_check_map)
                        shoot_list.append((0,0))
                        # map_list.append(trace[position[0]][position[1]][3])
                        map_list.append(temp_check_map)
                        temp_check_map = trace[position[0]][position[1]][3]
                        direction_list.append(trace[position[0]][position[1]][2])
                        direction_list.append(trace[position[0]][position[1]][2])
                        position = trace[position[0]][position[1]][0]
                        path.append(position)
                        check_sort = trace[position[0]][position[1]][1]
                        kiemtra = trace[position[0]][position[1]][4]
                    else:
                        path.append(position)
                        shoot_list.append((0,0))
                        direction_list.append(trace[position[0]][position[1]][2])
                        map_list.append(trace[position[0]][position[1]][3])
                        temp_check_map = trace[position[0]][position[1]][3]
                        position = trace[position[0]][position[1]][0]
                        check_sort = trace[position[0]][position[1]][1]
                        kiemtra = trace[position[0]][position[1]][4]
                path.append(start)
                path.reverse()
                shoot_list.reverse()
                direction_list.reverse()
                map_list.reverse()
                self.currentCave = start
                self.map_game=copy.deepcopy(old_map)
                self.knowledgePit=copy.deepcopy(old_knowPit)
                self.knowledgeWum=copy.deepcopy(old_knowWum)
                self.P=copy.deepcopy(old_p)
                self.W=copy.deepcopy(old_w)
                self.G=copy.deepcopy(old_g)
                self.direction= old_direction
                return path,shoot_list,direction_list,map_list, True
            dem_temp = 0
            for x_offset,y_offset in moves:
                print("Start end end")
                
                
                next_x, next_y = x + x_offset, y + y_offset
                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                    continue
                print(self.confirmPit(next_x,next_y))
                print(self.confirmWumpus(next_x,next_y))
                check_direction = "right"
                if (x_offset,y_offset) == (0,1):
                    check_direction = "right"
                elif (x_offset,y_offset) == (0,-1):
                    check_direction = "left"
                elif (x_offset,y_offset) == (-1,0):
                    check_direction = "up"
                elif (x_offset,y_offset) == (1,0):
                    check_direction = "down"
                old_map3 = copy.deepcopy(self.map_game)
                old_knowPit3 =copy.deepcopy(self.knowledgePit)
                old_knowWum3 = copy.deepcopy(self.knowledgeWum)
                old_p3 = copy.deepcopy(self.P)
                old_w3 = copy.deepcopy(self.W)
                old_g3 = copy.deepcopy(self.G)
                if self.confirmPit(next_x,next_y) == "0" and self.confirmWumpus(next_x,next_y) == "0" and visited[next_x][next_y] != 1:
                    if "G" in self.map_game[next_x][next_y]: 
                        print("Start end end 1")
                        frontier.put([cost-990,(next_x,next_y),(x,y),check_direction,0,old_map3,old_knowPit3,old_knowWum3,old_p3,old_w3,old_g3])
                        dem_temp += 1
                    else:
                        frontier.put([cost+10,(next_x,next_y),(x,y),check_direction,0,old_map3,old_knowPit3,old_knowWum3,old_p3,old_w3,old_g3])
                        dem_temp += 1
                if self.confirmWumpus(next_x,next_y) == "1" and visited[next_x][next_y] != 1 and self.confirmPit(next_x,next_y) == "0":
                    print("Start end end 2")
                    frontier.put([cost+110,(next_x,next_y),(x,y),check_direction,1,old_map3,old_knowPit3,old_knowWum3,old_p3,old_w3,old_g3])
                    dem_temp += 1
                if self.confirmWumpus(next_x,next_y) == "-1" and visited[next_x][next_y] != 1 and self.confirmPit(next_x,next_y) == "0":
                    print("Start end end 3")
                    frontier.put([cost+110,(next_x,next_y),(x,y),check_direction,1,old_map3,old_knowPit3,old_knowWum3,old_p3,old_w3,old_g3])
                    dem_temp += 1
            if dem_temp == 0:
                move_random = [(1,0),(0,-1)]
                next_x1, next_y1 = 0,0
                x_chek_ran, y_chek_ran = 0,0
                for random_x, random_y in move_random:
                    next_x1, next_y1 = x + random_x, y + random_y
                    if next_x1 < 0 or next_x1 >= self.size or next_y1 < 0 or next_y1 >= self.size:
                        continue
                    if next_x1 == x and next_y1 == y:
                        continue
                    x_chek_ran, y_chek_ran = random_x, random_y
                    break
                check_direction_ran = "right"
                if (x_chek_ran, y_chek_ran) == (0,1):
                    check_direction_ran = "right"
                elif (x_chek_ran, y_chek_ran) == (0,-1):
                    check_direction_ran = "left"
                elif (x_chek_ran, y_chek_ran) == (-1,0):
                    check_direction_ran = "up"
                elif (x_chek_ran, y_chek_ran) == (1,0):
                    check_direction_ran = "down"
                old_map3 = copy.deepcopy(self.map_game)
                old_knowPit3 =copy.deepcopy(self.knowledgePit)
                old_knowWum3 = copy.deepcopy(self.knowledgeWum)
                old_p3 = copy.deepcopy(self.P)
                old_w3 = copy.deepcopy(self.W)
                old_g3 = copy.deepcopy(self.G)
                if self.confirmPit(next_x1,next_y1) == "0":
                    frontier.put([cost+10,(next_x1,next_y1),(x,y),check_direction_ran,0,old_map3,old_knowPit3,old_knowWum3,old_p3,old_w3,old_g3]) 
            
        return path_save,shoot_list_save,direction_list_save,map_list_save, False

    def getPathCanGo(self,start,check_style,offset,direction,old):
        moves = [(-1, 0), (0, 1), (0, -1) ,(1, 0)]
        path_can_go = []
        kill_wumpus = []
        for x_offset, y_offset in moves:
            x_next, y_next = start[0] + x_offset, start[1] + y_offset
            check_direction = "right"
            if (x_offset,y_offset) == (0,1):
                check_direction = "right"
            elif (x_offset,y_offset) == (0,-1):
                check_direction = "left"
            elif (x_offset,y_offset) == (-1,0):
                check_direction = "up"
            elif (x_offset,y_offset) == (1,0):
                check_direction = "down"
            if check_style == 2:
                if x_offset == offset[0] and y_offset == offset[1]:
                    xynew = offset
                    if xynew == (0,1):
                        xynew = (0,-1)
                    elif xynew == (0,-1):
                        xynew = (0,1)
                    elif xynew == (-1,0):
                        xynew = (1,0)
                    elif xynew == (1,0):
                        xynew = (-1,0)
                    if start[0]+xynew[0] < 0 or start[0]+xynew[0] >= self.size or start[1]+xynew[1] < 0 or start[1]+xynew[1] >= self.size:
                        if self.try_stop == 0:
                            if self.end is not None:
                                temp_path,shoot_list,direction_list,map_list_return, exit_live = self.find_path_to_exit(start,(self.size-1,0))
                                # if temp_path is None and exit_live is False:
                                #     return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                                self.path.pop()
                                self.path.extend(temp_path)
                                self.map_list.extend(map_list_return)
                                path_exit = len(temp_path)
                                for i in range(1,path_exit):
                                    point_temp = self.point[-1]
                                    if shoot_list[i][0] == 1:
                                        point_temp -= 100
                                    if "G" in self.map_game[temp_path[i][0]][temp_path[i][1]] and self.G[temp_path[i][0]][temp_path[i][1]]!="1":
                                        point_temp += 1000
                                        self.G[temp_path[i][0]][temp_path[i][1]] = "1"
                                        self.grab.append(1)
                                    else:
                                        self.grab.append(0)
                                    if "P" in self.map_game[temp_path[i][0]][temp_path[i][1]]:
                                        point_temp -= 10000
                                    if "W" in self.map_game[temp_path[i][0]][temp_path[i][1]] and not exit_live:
                                        point_temp -= 10000
                                    if shoot_list[i][0] == 1:
                                        self.point.append(point_temp)
                                    else:
                                        self.point.append(point_temp-10)
                                if exit_live:
                                    self.point[-1] += 10
                                shoot_list = shoot_list[1:]
                                self.shoot.extend(shoot_list)
                                self.direction_list.extend(direction_list)
                                return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "Stop"
                            else:
                                print("Agent will not move when every cave is dangerous")
                                return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                        self.try_stop -= 1
                        if direction == "left":
                            go_max = [(1,0),(-1,0),(0,1),(0,-1)]
                            for move in go_max:
                                next_x, next_y = start[0] + move[0], start[1] + move[1]
                                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                    continue
                                xynew = move
                                check_unvisited = 0
                                for check_x,check_y in moves:
                                    check_next_x, check_next_y = start[0] + check_x, start[1] +check_y
                                    if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                        continue
                                    if self.visited[check_next_x][check_next_y] == "-1":
                                        check_unvisited += 1
                                if check_unvisited == 0:
                                    if self.confirmPit(start[0]+xynew[0],start[1]+xynew[1]) == "0":
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    self.visited[start[0]][start[1]] = "1"
                                break
                        elif direction == "right":
                            go_max = [(1,0),(-1,0),(0,1),(0,-1)]
                            for move in go_max:
                                next_x, next_y = start[0] + move[0], start[1] + move[1]
                                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                    continue
                                xynew = move
                                check_unvisited = 0
                                for check_x,check_y in moves:
                                    check_next_x, check_next_y = start[0] + check_x, start[1] +check_y
                                    if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                        continue
                                    if self.visited[check_next_x][check_next_y] == "-1":
                                        check_unvisited += 1
                                
                                if check_unvisited == 0:
                                    if self.confirmPit(start[0]+xynew[0],start[1]+xynew[1]) == "0":
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    self.visited[start[0]][start[1]] = "1"
                                break
                        elif direction == "up":
                            go_max = [(0,1),(0,-1),(1,0),(-1,0)]
                            for move in go_max:
                                next_x, next_y = start[0] + move[0], start[1] + move[1]
                                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                    continue
                                xynew = move
                                check_unvisited = 0
                                for check_x,check_y in moves:
                                    check_next_x, check_next_y = start[0] + check_x, start[1] +check_y
                                    if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                        continue
                                    if self.visited[check_next_x][check_next_y] == "-1":
                                        check_unvisited += 1
                                if check_unvisited == 0:
                                    if self.confirmPit(start[0]+xynew[0],start[1]+xynew[1]) == "0":
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    self.visited[start[0]][start[1]] = "1"
                                break
                        elif direction == "down":
                            go_max = [(0,1),(0,-1),(1,0),(-1,0)]
                            for move in go_max:
                                next_x, next_y = start[0] + move[0], start[1] + move[1]
                                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                    continue
                                xynew = move
                                check_unvisited = 0
                                for check_x,check_y in moves:
                                    check_next_x, check_next_y = start[0] + check_x, start[1] +check_y
                                    if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                        continue
                                    if self.visited[check_next_x][check_next_y] == "-1":
                                        check_unvisited += 1
                                if check_unvisited == 0:
                                    if self.confirmPit(start[0]+xynew[0],start[1]+xynew[1]) == "0":
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    self.visited[start[0]][start[1]] = "1"
                                break
                    if start[0]+xynew[0] >= 0 and start[0]+xynew[0] < self.size and start[1]+xynew[1] >= 0 and start[1]+xynew[1] < self.size:
                        
                        check_unvisited = 0
                        if direction == "left":
                            go_max = [(1,0),(-1,0)]
                            for move in go_max:
                                next_x, next_y = start[0] + move[0], start[1] + move[1]
                                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                    continue
                                xynew = move
                                check_unvisited = 0
                                for check_x,check_y in moves:
                                    check_next_x, check_next_y = start[0] + check_x, start[1] +check_y
                                    if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                        continue
                                    if self.visited[check_next_x][check_next_y] == "-1" and (check_next_x, check_next_y)!=old:
                                        check_unvisited += 1
                                if check_unvisited == 0:
                                    if self.try_stop == 0:
                                        if self.end is not None:
                                            temp_path,shoot_list,direction_list,map_list_return, exit_live = self.find_path_to_exit(start,(self.size-1,0))
                                            # if temp_path is None and exit_live is False:
                                            #     return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                                            self.path.pop()
                                            self.path.extend(temp_path)
                                            self.map_list.extend(map_list_return)
                                            path_exit = len(temp_path)
                                            for i in range(1,path_exit):
                                                point_temp = self.point[-1]
                                                if shoot_list[i][0] == 1:
                                                    point_temp -= 100
                                                if "G" in self.map_game[temp_path[i][0]][temp_path[i][1]] and self.G[temp_path[i][0]][temp_path[i][1]]!="1":
                                                    point_temp += 1000
                                                    self.G[temp_path[i][0]][temp_path[i][1]] = "1"
                                                    self.grab.append(1)
                                                else:
                                                    self.grab.append(0)
                                                if "P" in self.map_game[temp_path[i][0]][temp_path[i][1]]:
                                                    point_temp -= 10000
                                                if "W" in self.map_game[temp_path[i][0]][temp_path[i][1]] and not exit_live:
                                                    point_temp -= 10000
                                                if shoot_list[i][0] == 1:
                                                    self.point.append(point_temp)
                                                else:
                                                    self.point.append(point_temp-10)
                                            if exit_live:
                                                self.point[-1] += 10
                                            shoot_list = shoot_list[1:]
                                            self.shoot.extend(shoot_list)
                                            self.direction_list.extend(direction_list)
                                            return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "Stop"
                                        else:
                                            print("Agent will not move when every cave is dangerous")
                                            return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                                    self.try_stop -= 1
                                    if self.confirmPit(start[0]+xynew[0],start[1]+xynew[1]) == "0":
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    self.visited[start[0]][start[1]] = "1"
                                break
                        elif direction == "right":
                            go_max = [(-1,0),(1,0)]
                            for move in go_max:
                                next_x, next_y = start[0] + move[0], start[1] + move[1]
                                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                    continue
                                xynew = move
                                check_unvisited = 0
                                for check_x,check_y in moves:
                                    check_next_x, check_next_y = start[0] + check_x, start[1] +check_y
                                    if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                        continue
                                    if self.visited[check_next_x][check_next_y] == "-1":
                                        check_unvisited += 1
                                
                                if check_unvisited == 0:
                                    if self.try_stop == 0:
                                        if self.end is not None:
                                            temp_path,shoot_list,direction_list,map_list_return, exit_live = self.find_path_to_exit(start,(self.size-1,0))
                                            # if temp_path is None and exit_live is False:
                                            #     return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                                            self.path.pop()
                                            self.path.extend(temp_path)
                                            self.map_list.extend(map_list_return)
                                            path_exit = len(temp_path)
                                            for i in range(1,path_exit):
                                                point_temp = self.point[-1]
                                                if shoot_list[i][0] == 1:
                                                    point_temp -= 100
                                                if "G" in self.map_game[temp_path[i][0]][temp_path[i][1]] and self.G[temp_path[i][0]][temp_path[i][1]]!="1":
                                                    point_temp += 1000
                                                    self.G[temp_path[i][0]][temp_path[i][1]] = "1"
                                                    self.grab.append(1)
                                                else:
                                                    self.grab.append(0)
                                                if "P" in self.map_game[temp_path[i][0]][temp_path[i][1]]:
                                                    point_temp -= 10000
                                                if "W" in self.map_game[temp_path[i][0]][temp_path[i][1]] and not exit_live:
                                                    point_temp -= 10000
                                                if shoot_list[i][0] == 1:
                                                    self.point.append(point_temp)
                                                else:
                                                    self.point.append(point_temp-10)
                                            if exit_live:
                                                self.point[-1] += 10
                                            shoot_list = shoot_list[1:]
                                            self.shoot.extend(shoot_list)
                                            self.direction_list.extend(direction_list)
                                            return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "Stop"
                                        else:
                                            print("Agent will not move when every cave is dangerous")
                                            return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                                    self.try_stop -= 1
                                    if self.confirmPit(start[0]+xynew[0],start[1]+xynew[1]) == "0":
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    self.visited[start[0]][start[1]] = "1"
                                break
                        elif direction == "up":
                            go_max = [(0,-1),(0,1)]
                            for move in go_max:
                                next_x, next_y = start[0] + move[0], start[1] + move[1]
                                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                    continue
                                xynew = move
                                check_unvisited = 0
                                for check_x,check_y in moves:
                                    check_next_x, check_next_y = start[0] + check_x, start[1] +check_y
                                    if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                        continue
                                    if self.visited[check_next_x][check_next_y] == "-1":
                                        check_unvisited += 1
                                if check_unvisited == 0:
                                    if self.try_stop == 0:
                                        if self.end is not None:
                                            temp_path,shoot_list,direction_list,map_list_return, exit_live = self.find_path_to_exit(start,(self.size-1,0))
                                            # if temp_path is None and exit_live is False:
                                            #     return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                                            self.path.pop()
                                            self.path.extend(temp_path)
                                            self.map_list.extend(map_list_return)
                                            path_exit = len(temp_path)
                                            for i in range(1,path_exit):
                                                point_temp = self.point[-1]
                                                if shoot_list[i][0] == 1:
                                                    point_temp -= 100
                                                if "G" in self.map_game[temp_path[i][0]][temp_path[i][1]] and self.G[temp_path[i][0]][temp_path[i][1]]!="1":
                                                    point_temp += 1000
                                                    self.G[temp_path[i][0]][temp_path[i][1]] = "1"
                                                    self.grab.append(1)
                                                else:
                                                    self.grab.append(0)
                                                if "P" in self.map_game[temp_path[i][0]][temp_path[i][1]]:
                                                    point_temp -= 10000
                                                if "W" in self.map_game[temp_path[i][0]][temp_path[i][1]] and not exit_live:
                                                    point_temp -= 10000
                                                if shoot_list[i][0] == 1:
                                                    self.point.append(point_temp)
                                                else:
                                                    self.point.append(point_temp-10)
                                            if exit_live:
                                                self.point[-1] += 10
                                            shoot_list = shoot_list[1:]
                                            self.shoot.extend(shoot_list)
                                            self.direction_list.extend(direction_list)
                                            return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "Stop"
                                        else:
                                            print("Agent will not move when every cave is dangerous")
                                            return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                                    self.try_stop -= 1
                                    if self.confirmPit(start[0]+xynew[0],start[1]+xynew[1]) == "0":
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    self.visited[start[0]][start[1]] = "1"
                                break
                        elif direction == "down":
                            go_max = [(0,1),(0,-1)]
                            for move in go_max:
                                next_x, next_y = start[0] + move[0], start[1] + move[1]
                                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                    continue
                                xynew = move
                                check_unvisited = 0
                                for check_x,check_y in moves:
                                    check_next_x, check_next_y = start[0] + check_x, start[1] +check_y
                                    if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                        continue
                                    if self.visited[check_next_x][check_next_y] == "-1":
                                        check_unvisited += 1
                                if check_unvisited == 0:
                                    if self.try_stop == 0:
                                        if self.end is not None:
                                            temp_path,shoot_list,direction_list,map_list_return, exit_live = self.find_path_to_exit(start,(self.size-1,0))
                                            # if temp_path is None and exit_live is False:
                                            #     return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                                            self.path.pop()
                                            self.path.extend(temp_path)
                                            self.map_list.extend(map_list_return)
                                            path_exit = len(temp_path)
                                            for i in range(1,path_exit):
                                                point_temp = self.point[-1]
                                                if shoot_list[i][0] == 1:
                                                    point_temp -= 100
                                                if "G" in self.map_game[temp_path[i][0]][temp_path[i][1]] and self.G[temp_path[i][0]][temp_path[i][1]]!="1":
                                                    point_temp += 1000
                                                    self.G[temp_path[i][0]][temp_path[i][1]] = "1"
                                                    self.grab.append(1)
                                                else:
                                                    self.grab.append(0)
                                                if "P" in self.map_game[temp_path[i][0]][temp_path[i][1]]:
                                                    point_temp -= 10000
                                                if "W" in self.map_game[temp_path[i][0]][temp_path[i][1]] and not exit_live:
                                                    point_temp -= 10000
                                                if shoot_list[i][0] == 1:
                                                    self.point.append(point_temp)
                                                else:
                                                    self.point.append(point_temp-10)
                                            if exit_live:
                                                self.point[-1] += 10
                                            shoot_list = shoot_list[1:]
                                            self.shoot.extend(shoot_list)
                                            self.direction_list.extend(direction_list)
                                            return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "Stop"
                                        else:
                                            print("Agent will not move when every cave is dangerous")
                                            return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                                    self.try_stop -= 1
                                    if self.confirmPit(start[0]+xynew[0],start[1]+xynew[1]) == "0":
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    self.visited[start[0]][start[1]] = "1"
                                break
            if x_next < 0 or x_next >= self.size or y_next < 0 or y_next >= self.size:
                continue
            if self.confirmPit(x_next,y_next) == "0" and self.confirmWumpus(x_next,y_next) == "0" and self.visited[x_next][y_next] == "-1":
                path_can_go.append((x_next,y_next,0,(x_offset,y_offset),check_direction,copy.deepcopy(self.map_game)))
            if self.confirmWumpus(x_next,y_next) == "1" and self.visited[x_next][y_next] == "-1" and self.confirmPit(x_next,y_next) == "0":
                kill_wumpus.append((x_next,y_next,1, (x_offset,y_offset),check_direction,copy.deepcopy(self.map_game)))
            if self.confirmWumpus(x_next,y_next) == "-1" and self.visited[x_next][y_next] == "-1" and self.confirmPit(x_next,y_next) == "0":
                kill_wumpus.append((x_next,y_next,1, (x_offset,y_offset),check_direction,copy.deepcopy(self.map_game)))
        if len(kill_wumpus) != 0:
                path_can_go.extend(kill_wumpus)
        if len(path_can_go) == 0 and old != (-1,-1):
            self.try_stop -= 1
            if self.try_stop <= 0:
                temp_path,shoot_list,direction_list,map_list_return, exit_live = self.find_path_to_exit(start,(self.size-1,0))
                if temp_path is None and exit_live is False:
                    return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
                self.path.pop()
                self.path.extend(temp_path)
                self.map_list.extend(map_list_return)
                path_exit = len(temp_path)
                for i in range(1,path_exit):
                    point_temp = self.point[-1]
                    if shoot_list[i][0] == 1:
                        point_temp -= 100
                    if "G" in self.map_game[temp_path[i][0]][temp_path[i][1]] and self.G[temp_path[i][0]][temp_path[i][1]]!="1":
                        point_temp += 1000
                        self.G[temp_path[i][0]][temp_path[i][1]] = "1"
                        self.grab.append(1)
                    else:
                        self.grab.append(0)
                    if "P" in self.map_game[temp_path[i][0]][temp_path[i][1]]:
                        point_temp -= 10000
                    if "W" in self.map_game[temp_path[i][0]][temp_path[i][1]] and not exit_live:
                        point_temp -= 10000
                    if shoot_list[i][0] == 1:
                        self.point.append(point_temp)
                    else:
                        self.point.append(point_temp-10)
                if exit_live:
                    self.point[-1] += 10
                shoot_list = shoot_list[1:]
                self.shoot.extend(shoot_list)
                self.direction_list.extend(direction_list)
                return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "Stop"
            xynew = (start[0]-old[0],start[1]-old[1])
            direction_go = "right"
            if xynew == (0,1):
                xynew = (0,-1)
                direction_go = "left"
            elif xynew == (0,-1):
                xynew = (0,1)
                direction_go = "right"
            elif xynew == (-1,0):
                xynew = (1,0)
                direction_go = "down"
            elif xynew == (1,0):
                xynew = (-1,0)
                direction_go = "up"
            if len(kill_wumpus) == 0 and check_style != 2:
                if self.confirmPit(old[0],old[1]) == "0":
                    path_can_go.append((old[0],old[1],2,(start[0]-old[0],start[1]-old[1]),direction_go,copy.deepcopy(self.map_game)))
            elif len(kill_wumpus) == 0 and check_style == 2:
                if self.confirmPit(old[0],old[1]) == "0":
                    path_can_go.append((old[0],old[1],2,(start[0]-old[0],start[1]-old[1]),direction_go,copy.deepcopy(self.map_game)))
                if old[0]+xynew[0] < 0 or old[0]+xynew[0] >= self.size or old[1]+xynew[1] < 0 or old[1]+xynew[1] >= self.size:
                    if direction_go == "left":
                        go_max = [(1,0),(-1,0),(0,1),(0,-1)]
                        for move in go_max:
                            next_x, next_y = old[0] + move[0], old[1] + move[1]
                            if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                continue
                            xynew = move
                            check_unvisited = 0
                            for check_x,check_y in moves:
                                check_next_x, check_next_y = old[0] + check_x, old[1] +check_y
                                if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                    continue
                                if self.visited[check_next_x][check_next_y] == "-1":
                                    check_unvisited += 1
                            
                            if check_unvisited == 0:
                                if self.confirmPit(old[0]+xynew[0],old[1]+xynew[1]) == "0":
                                    self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                                self.visited[old[0]][old[1]] = "1"
                            break
                    elif direction_go == "right":
                        go_max = [(1,0),(-1,0),(0,1),(0,-1)]
                        for move in go_max:
                            next_x, next_y = old[0] + move[0], old[1] + move[1]
                            if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                continue
                            xynew = move
                            check_unvisited = 0
                            for check_x,check_y in moves:
                                check_next_x, check_next_y = old[0] + check_x, old[1] +check_y
                                if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                    continue
                                if self.visited[check_next_x][check_next_y] == "-1":
                                    check_unvisited += 1
                            if check_unvisited == 0:
                                if self.confirmPit(old[0]+xynew[0],old[1]+xynew[1]) == "0":
                                    self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                                self.visited[old[0]][old[1]] = "1"
                            break
                    elif direction_go == "up":
                        go_max = [(0,1),(0,-1),(1,0),(-1,0)]
                        for move in go_max:
                            next_x, next_y = old[0] + move[0], old[1] + move[1]
                            if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                continue
                            xynew = move
                            
                            check_unvisited = 0
                            for check_x,check_y in moves:
                                check_next_x, check_next_y = old[0] + check_x, old[1] +check_y
                                
                                if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                    continue
                                
                                if self.visited[check_next_x][check_next_y] == "-1":
                                    check_unvisited += 1
                            
                            if check_unvisited == 0:
                                if self.confirmPit(old[0]+xynew[0],old[1]+xynew[1]) == "0":
                                    self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                                self.visited[old[0]][old[1]] = "1"
                            break
                    elif direction_go == "down":
                        go_max = [(0,1),(0,-1),(1,0),(-1,0)]
                        for move in go_max:
                            next_x, next_y = old[0] + move[0], old[1] + move[1]
                            if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                                continue
                            xynew = move
                            
                            check_unvisited = 0
                            for check_x,check_y in moves:
                                check_next_x, check_next_y = old[0] + check_x, old[1] +check_y
                                
                                if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                    continue
                                
                                if self.visited[check_next_x][check_next_y] == "-1":
                                    check_unvisited += 1
                            
                            if check_unvisited == 0:
                                if self.confirmPit(old[0]+xynew[0],old[1]+xynew[1]) == "0":
                                    self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                                self.visited[old[0]][old[1]] = "1"
                            break
                else:
                    if self.confirmPit(old[0]+xynew[0],old[1]+xynew[1]) == "0":
                        self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                    self.visited[old[0]][old[1]] = "1"
        if len(path_can_go) == 0 and old == (-1,-1):
            print("Agent will not move when every cave is dangerous")
            return self.path,self.point,self.shoot,self.direction_list,self.grab,self.map_list, "StopUnsure"
        return path_can_go,"Continue"

