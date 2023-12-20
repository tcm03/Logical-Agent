from queue import PriorityQueue
import random
import copy


class Agent:
    def __init__(self,x,y,N,map_game):
        self.map_game = map_game
        self.currentCave = (x,y)
        self.direction = "right"
        self.P = [] # matrix to save the move 
        self.G = []
        self.W = []
        self.visited = []
        self.size = N
        self.knowledgePit = []
        self.knowledgeWum = []
        self.path = []
        self.point = [0]
        self.shoot = []
        self.try_stop = 1
        self.direction_list=[]
        self.grab = []
        
        
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
            
    
    def find_path_to_exit(self, start, end):
        trace = []
        visited = []

        for _ in range(self.size):
            temp = []
            temp_visited = []
            for _ in range(self.size):
                temp.append(((-1,-1),0))
                temp_visited.append(False)
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
        moves = [(0, 1), (0, -1), (-1, 0),(1, 0)]
        while True:
            cost, position ,old_position, direction,is_shoot,old_map2,old_knowPit2,old_knowWum2,old_p2,old_w2,old_g2 = frontier.get()
            self.currentCave = position
            self.map_game=old_map2
            self.knowledgePit=old_knowPit2
            self.knowledgeWum=old_knowWum2
            self.P=old_p2
            self.W=old_w2
            self.G=old_g2
            self.direction= direction
            
            if is_shoot == 1:
                kiemtra = self.confirmScream()
                if kiemtra:
                    self.updateMap()
            self.perceive()
            x, y = position
            if visited[x][y]:
                continue
            visited[x][y] = True
            trace[x][y] = (old_position,is_shoot,direction)
            if self.map_game[x][y] == "P" or ("W" in self.map_game[x][y] and is_shoot == 0):
                path = []
                shoot_list = [is_shoot]
                direction_list = [direction]
                check_sort = is_shoot
                while position != start:  # change here
                    if check_sort == 1:
                        path.append(position)
                        path.append(position)
                        print(position)
                        shoot_list.append(1)
                        shoot_list.append(0)
                        direction_list.append(trace[position[0]][position[1]][2])
                        direction_list.append(trace[position[0]][position[1]][2])
                        position = trace[position[0]][position[1]][0]
                        check_sort = trace[position[0]][position[1]][1]
                    else:
                        path.append(position)
                        position = trace[position[0]][position[1]][0]
                        shoot_list.append(0)
                        direction_list.append(trace[position[0]][position[1]][2])
                        check_sort = trace[position[0]][position[1]][1]
                path.append(start)  # add start to the path
                path.reverse()  # reverse the path to get from start to end
                shoot_list.reverse()
                direction_list.reverse()
                self.currentCave = start
                self.map_game=old_map
                self.knowledgePit=old_knowPit
                self.knowledgeWum=old_knowWum
                self.P=old_p
                self.W=old_w
                self.G=old_g
                self.direction= old_direction
                
                return path,shoot_list,direction_list, False

            if position == end:
                path = []
                shoot_list = [is_shoot]
                direction_list = [direction]
                check_sort = is_shoot
                while position != start:  # change here
                    
                    if check_sort == 1:
                        path.append(position)
                        path.append(position)
                        shoot_list.append(1)
                        shoot_list.append(0)
                        direction_list.append(trace[position[0]][position[1]][2])
                        direction_list.append(trace[position[0]][position[1]][2])
                        position = trace[position[0]][position[1]][0]
                        check_sort = trace[position[0]][position[1]][1]
                    else:
                        path.append(position)
                        position = trace[position[0]][position[1]][0]
                        shoot_list.append(0)
                        direction_list.append(trace[position[0]][position[1]][2])
                        check_sort = trace[position[0]][position[1]][1]
                path.append(start)  # add start to the path
                path.reverse()  # reverse the path to get from start to end
                shoot_list.reverse()
                direction_list.reverse()
                self.currentCave = start
                self.map_game=old_map
                self.knowledgePit=old_knowPit
                self.knowledgeWum=old_knowWum
                self.P=old_p
                self.W=old_w
                self.G=old_g
                self.direction= old_direction
                
                return path,shoot_list,direction_list, True
                
            dem_temp = 0
            for x_offset,y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset
                check_direction = "right"
                if (x_offset,y_offset) == (0,1):
                    check_direction = "right"
                elif (x_offset,y_offset) == (0,-1):
                    check_direction = "left"
                elif (x_offset,y_offset) == (-1,0):
                    check_direction = "top"
                elif (x_offset,y_offset) == (1,0):
                    check_direction = "down"

                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                    continue

                
                old_map3 = copy.deepcopy(self.map_game)
                old_knowPit3 =copy.deepcopy(self.knowledgePit)
                old_knowWum3 = copy.deepcopy(self.knowledgeWum)
                old_p3 = copy.deepcopy(self.P)
                old_w3 = copy.deepcopy(self.W)
                old_g3 = copy.deepcopy(self.G)
                
                
                if self.confirmPit(next_x,next_y) == "0" and self.confirmWumpus(next_x,next_y) == "0" and visited[next_x][next_y] != True:
                    frontier.put([cost+1,(next_x,next_y),(x,y),check_direction,0,old_map3,old_knowPit3,old_knowWum3,old_p3,old_w3,old_g3])
                    dem_temp += 1
                    
                if self.confirmWumpus(next_x,next_y) == "1" and visited[next_x][next_y] != True:
                    frontier.put([cost+100,(next_x,next_y),(x,y),check_direction,1,old_map3,old_knowPit3,old_knowWum3,old_p3,old_w3,old_g3])
                    dem_temp += 1
                    
                if self.confirmWumpus(next_x,next_y) == "-1" and visited[next_x][next_y] != True:
                    frontier.put([cost+100,(next_x,next_y),(x,y),check_direction,1,old_map3,old_knowPit3,old_knowWum3,old_p3,old_w3,old_g3])
                    dem_temp += 1
                    
                        
            if dem_temp == 0:
                move_random = [(1,0),(0,-1)]
                for random_x, random_y in move_random:
                    next_x1, next_y1 = x + random_x, y + random_y
                    if next_x1 < 0 or next_x1 >= self.size or next_y1 < 0 or next_y1 >= self.size:
                        continue
                    if next_x1 == x and next_y1 == y:
                        continue
                    break
                
                check_direction_ran = "right"
                if (x_offset,y_offset) == (0,1):
                    check_direction_ran = "right"
                elif (x_offset,y_offset) == (0,-1):
                    check_direction_ran = "left"
                elif (x_offset,y_offset) == (-1,0):
                    check_direction_ran = "top"
                elif (x_offset,y_offset) == (1,0):
                    check_direction_ran = "down"
                    
                old_map3 = copy.deepcopy(self.map_game)
                old_knowPit3 =copy.deepcopy(self.knowledgePit)
                old_knowWum3 = copy.deepcopy(self.knowledgeWum)
                old_p3 = copy.deepcopy(self.P)
                old_w3 = copy.deepcopy(self.W)
                old_g3 = copy.deepcopy(self.G)
                
                frontier.put([cost+1,(next_x1,next_y1),(x,y),check_direction_ran,0,old_map3,old_knowPit3,old_knowWum3,old_p3,old_w3,old_g3]) 

    def perceive(self):
        moves = [(0, 1), (0, -1), (-1, 0),(1, 0)]
        
        x, y = self.currentCave
        
        if self.map_game[x][y] == "-" or self.map_game[x][y] == "G":
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset

                # invalid next cell
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
        
        #check Pit logic
        if "B" in self.map_game[x][y]:
            # print("co B va S")
            # print("xet B")
            createLogicPit = []
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset

                # invalid next cell
                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                    continue
                
                if self.confirmPit(next_x,next_y) == "-1":
                    createLogicPit.append((next_x,next_y,-1))
                if self.confirmPit(next_x,next_y) == "1":
                    createLogicPit.append((next_x,next_y,1))
                    
            if len(createLogicPit) == 1:
                # the cave is Pit
                if createLogicPit[0][2] == -1:
                    self.updatePit(createLogicPit[0][0],createLogicPit[0][1],"1")
            else:
                string_logic = ""
                for cave in createLogicPit:
                    string_logic += f"{cave[0]},{cave[1]}?"
                self.knowledgePit.append(string_logic)
                
        #check Wumpus logic
        if "S" in self.map_game[x][y]:
            # print("Xet S")
            createLogicWum = []
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset
                
                #invalid next cell
                if next_x < 0 or next_x >= self.size or next_y < 0 or next_y >= self.size:
                    continue
                
                if self.confirmWumpus(next_x,next_y) == "-1":
                    createLogicWum.append((next_x,next_y,-1))
                if self.confirmWumpus(next_x,next_y) == "1":
                    createLogicWum.append((next_x,next_y,1))
                    
                if len(createLogicWum) == 1:
                    #the cave is Wumpus
                    if createLogicWum[0][2] == -1:
                        self.updateWumPus(createLogicWum[0][0],createLogicWum[0][1],"1")
                else:
                    string_logic = ""
                    for cave in createLogicWum:
                        string_logic += f"{cave[0]},{cave[1]}?"
                    self.knowledgeWum.append(string_logic)
            
        #check only Pit but not Wumpus
        if "S" not in self.map_game[x][y]:
            # print("Co B khong S")
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset

                # invalid next cell
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
                        
        #check only Wumpus but not Pit
        if "B" not in self.map_game[x][y]:
            # print("Co S khong B")
            for x_offset, y_offset in moves:
                next_x, next_y = x + x_offset, y + y_offset
                # invalid next cell
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
        
    def confirmScream(self):
        if self.direction == "left":
            for i in range(self.currentCave[1],-1,-1):
                if "W" in self.map_game[self.currentCave[0]][i]:
                    # self.updateWumPus(self.currentCave[0],i,"0")
                    self.updateWumPus(self.currentCave[0],self.currentCave[1]-1,"0")
                    self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                    txt = self.map_game[self.currentCave[0]][i]
                    temp = txt[0:txt.index("W")]+txt[txt.index("W")+1:]
                    self.map_game[self.currentCave[0]][i]=temp
                    if self.map_game[self.currentCave[0]][i] == "":
                        
                        self.map_game[self.currentCave[0]][i]='-'
                    return True
        if self.direction == "right":
            for i in range(self.currentCave[1],self.size):
                if "W" in self.map_game[self.currentCave[0]][i]:
                    # self.updateWumPus(self.currentCave[0],i,"0")
                    self.updateWumPus(self.currentCave[0],self.currentCave[1]+1,"0")
                    self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                    txt = self.map_game[self.currentCave[0]][i]
                    temp = txt[0:txt.index("W")]+txt[txt.index("W")+1:]
                    self.map_game[self.currentCave[0]][i]=temp
                    if self.map_game[self.currentCave[0]][i] == "":
                        self.map_game[self.currentCave[0]][i]='-'
                    return True
        if self.direction == "up":
            for i in range(self.currentCave[0],-1,-1):
                if "W" in self.map_game[i][self.currentCave[1]]:
                    # self.updateWumPus(i,self.currentCave[1],"0")
                    self.updateWumPus(self.currentCave[0]-1,self.currentCave[1],"0")
                    self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                    txt = self.map_game[i][self.currentCave[1]]
                    temp = txt[0:txt.index("W")]+txt[txt.index("W")+1:]
                    self.map_game[i][self.currentCave[1]]=temp
                    if self.map_game[i][self.currentCave[1]] == "":
                        self.map_game[i][self.currentCave[1]]='-'
                    return True
        if self.direction == "down":
            for i in range(self.currentCave[0],self.size):
                if "W" in self.map_game[i][self.currentCave[1]]:
                    # self.updateWumPus(i,self.currentCave[1],"0")
                    self.updateWumPus(self.currentCave[0]+1,self.currentCave[1],"0")
                    self.updateWumPus(self.currentCave[0],self.currentCave[1],"0")
                    txt = self.map_game[i][self.currentCave[1]]
                    temp = txt[0:txt.index("W")]+txt[txt.index("W")+1:]
                    self.map_game[i][self.currentCave[1]]=temp
                    if self.map_game[i][self.currentCave[1]] == "":
                        self.map_game[i][self.currentCave[1]]='-'
                    return True
        
        if self.direction == "left":
            for i in range(self.currentCave[1],-1,-1):
                self.updateWumPus(self.currentCave[0],i,"0")
        if self.direction == "right":
            for i in range(self.currentCave[1],self.size):
                self.updateWumPus(self.currentCave[0],i,"0")
                    
        if self.direction == "top":
            for i in range(self.currentCave[0],-1,-1):
                self.updateWumPus(i,self.currentCave[1],"0")
        if self.direction == "down":
            for i in range(self.currentCave[0],self.size):
                self.updateWumPus(i,self.currentCave[1],"0")
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

    
    def find_path(self,start,old,check_style,offset,direction):
        
        self.currentCave = start
        if old == (-1,-1):
            self.P[start[0]][start[1]] = "0"
            self.W[start[0]][start[1]] = "0"
            if "G" in self.map_game[start[0]][start[1]] and self.G[start[0]][start[1]] != "1":
                self.grab.append(1)
            else:
                self.grab.append(0)
        old_matrix_pit = copy.deepcopy(self.P)
        old_matrix_wum = copy.deepcopy(self.W)
        old_knowledge_pit = copy.deepcopy(self.knowledgePit)
        old_knowledge_wum = copy.deepcopy(self.knowledgeWum)
        old_map = copy.deepcopy(self.map_game)
        old_try = self.try_stop
        old_point = copy.deepcopy(self.point)
        old_shoot = copy.deepcopy(self.shoot)
        old_path = copy.deepcopy(self.path)
        old_direction_list = copy.deepcopy(self.direction_list)
        old_grab = copy.deepcopy(self.grab)
        
        temp_point = self.point[-1]
        
        self.direction = direction
        if check_style == 1:
            temp_point -= 100
            self.path.append(start)
            self.direction_list.append(direction)
            self.point.append(temp_point)
            is_scream = self.confirmScream()
            if is_scream:
                self.updateMap()
                
            if "G" in self.map_game[start[0]][start[1]] and self.G[start[0]][start[1]] != "1":
                self.grab.append(1)
            else:
                self.grab.append(0)
                
        
        
        self.perceive()
        self.visited[start[0]][start[1]] = "1"
        self.path.append(start)
        self.direction_list.append(direction)
        
        
        if check_style == 1:
            self.shoot.append(1)
            self.shoot.append(0)
        else:
            self.shoot.append(0)
            
        # if "G" in self.map_game[start[0]][start[1]] and self.G[start[0]][start[1]] != "1":
        #     self.grab.append(1)
        # else:
        #     self.grab.append(0)
        
        if old != (-1,-1):
            if "P" in self.map_game[start[0]][start[1]]:
                temp_point -= 10000
            if "G" in self.map_game[start[0]][start[1]] and self.G[start[0]][start[1]] != "1":
                temp_point += 1000
                self.grab.append(1)
            else:
                self.grab.append(0)
            if "W" in self.map_game[start[0]][start[1]]:
                temp_point -= 10000
            temp_point -= 10
        
        if old != (-1,-1):
            self.point.append(temp_point)
        
        if "P" in self.map_game[start[0]][start[1]] or "W" in self.map_game[start[0]][start[1]]:
            return self.path,self.point,self.shoot,self.direction_list,self.grab, "Stop"
        
        if "G" in self.map_game[start[0]][start[1]]:
            self.G[start[0]][start[1]] = "1"
            temp_path,shoot_list,direction_list, exit_live = self.find_path_to_exit(start,(self.size-1,0))
            self.path.pop()
            self.path.extend(temp_path)
            path_exit = len(temp_path)
            for i in range(1,path_exit):
                point_temp = self.point[-1]
                # is_fire = True
                if shoot_list[i] == 1:
                    point_temp -= 100
                    
                    # self.shoot.append(1)
                    # is_fire = False
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
                if shoot_list[i] == 1:
                    self.point.append(point_temp)
                else:
                    self.point.append(point_temp-10)
                # if is_fire:
                #     self.shoot.append(0)
            if exit_live:
                self.point[-1] += 10
            shoot_list = shoot_list[1:]
            direction_list = direction_list[1:]
            self.shoot.extend(shoot_list)
            self.direction_list.extend(direction_list)
            return self.path,self.point,self.shoot,self.direction_list,self.grab, "Stop"
        else:
            moves = [(0, 1), (0, -1), (-1, 0),(1, 0)]
            
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
                    check_direction = "top"
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
                                temp_path,shoot_list,direction_list, exit_live = self.find_path_to_exit(start,(self.size-1,0))
                                self.path.pop()
                                self.path.extend(temp_path)
                                path_exit = len(temp_path)
                                for i in range(1,path_exit):
                                    point_temp = self.point[-1]
                                    # is_fire = True
                                    if shoot_list[i] == 1:
                                        point_temp -= 100
                                        # self.shoot.append(1)
                                        # is_fire = False
                                    if "G" in self.map_game[temp_path[i][0]][temp_path[i][1]] and self.G[temp_path[i][0]][temp_path[i][1]]!="1":
                                        point_temp += 1000
                                        self.G[temp_path[i][0]][temp_path[i][0]] = "1"
                                        self.grab.append(1)
                                    else:
                                        self.grab.append(0)
                                    if "P" in self.map_game[temp_path[i][0]][temp_path[i][1]]:
                                        point_temp -= 10000
                                    if "W" in self.map_game[temp_path[i][0]][temp_path[i][1]] and not exit_live:
                                        point_temp -= 10000
                                    if shoot_list[i] == 1:
                                        self.point.append(point_temp)
                                    else:
                                        self.point.append(point_temp-10)
                                    # if is_fire:
                                    #     self.shoot.append(0)
                                if exit_live:
                                    self.point[-1] += 10
                                shoot_list = shoot_list[1:]
                                direction_list = direction_list[1:]
                                self.shoot.extend(shoot_list)
                                self.direction_list.extend(direction_list)
                                return self.path,self.point,self.shoot,self.direction_list,self.grab, "Stop"
                            self.try_stop -= 1
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
                                        
                                        if self.visited[check_next_x][check_next_y] == "-1":
                                            check_unvisited += 1
                                    
                                    if check_unvisited == 0:
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    break
                            elif direction == "right":
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
                                        
                                        if self.visited[check_next_x][check_next_y] == "-1":
                                            check_unvisited += 1
                                    
                                    if check_unvisited == 0:
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    break
                            elif direction == "top":
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
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
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
                                        self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                                    break
                        else:
                            check_unvisited = 0
                            for check_x,check_y in moves:
                                check_next_x, check_next_y = start[0] + check_x, start[1] +check_y
                                
                                if check_next_x < 0 or check_next_x >= self.size or check_next_y < 0 or check_next_y >= self.size:
                                    continue
                                
                                if self.visited[check_next_x][check_next_y] == "-1":
                                    check_unvisited += 1
                            
                            if check_unvisited == 0:
                                self.visited[start[0]+xynew[0]][start[1]+xynew[1]] = "-1"
                
                # invalid next cell
                if x_next < 0 or x_next >= self.size or y_next < 0 or y_next >= self.size:
                    continue
                
                
                if self.confirmPit(x_next,y_next) == "0" and self.confirmWumpus(x_next,y_next) == "0" and self.visited[x_next][y_next] == "-1":
                    path_can_go.append((x_next,y_next,0,(x_offset,y_offset),check_direction))
                    
                if self.confirmWumpus(x_next,y_next) == "1" and self.visited[x_next][y_next] == "-1":
                    kill_wumpus.append((x_next,y_next,1, (x_offset,y_offset),check_direction))
                    
            if len(path_can_go) == 0:
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
                    direction_go = "top"
                if len(kill_wumpus) == 0 and check_style != 2:
                    path_can_go.append((old[0],old[1],2,(start[0]-old[0],start[1]-old[1]),direction_go))
                elif len(kill_wumpus) == 0 and check_style == 2:
                    path_can_go.append((old[0],old[1],2,(start[0]-old[0],start[1]-old[1]),direction_go))
                    if old[0]+xynew[0] < 0 or old[0]+xynew[0] >= self.size or old[1]+xynew[1] < 0 or old[1]+xynew[1] >= self.size:
                        if direction_go == "left":
                            go_max = [(1,0),(-1,0)]
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
                                    self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                                break
                        elif direction_go == "right":
                            go_max = [(1,0),(-1,0)]
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
                                    self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                                break
                        elif direction_go == "top":
                            go_max = [(0,1),(0,-1)]
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
                                    self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                                break
                        elif direction_go == "down":
                            go_max = [(0,1),(0,-1)]
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
                                    self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                                break
                    else:
                        self.visited[old[0]+xynew[0]][old[1]+xynew[1]] = "-1"
                if len(kill_wumpus) != 0:
                    path_can_go.extend(kill_wumpus)

            for step in path_can_go:
                path_find, point_path,fire,list_direction,grab, check = self.find_path((step[0],step[1]),start,step[2],step[3],step[4])
                if check == "Stop":
                    return path_find,point_path,fire,list_direction,grab, "Stop"
                self.P = old_matrix_pit
                self.W = old_matrix_wum
                self.knowledgePit = old_knowledge_pit
                self.knowledgeWum = old_knowledge_wum
                self.map_game = old_map
                self.try_stop = old_try
                self.point = old_point
                self.shoot = old_shoot
                self.path = old_path
                self.direction_list=old_direction_list
                self.grab = old_grab
                self.path.pop()
            
            
            self.visited[start[0]][start[1]] = "-1"
            
    
    
    def updatePit(self, x, y, check):
        self.P[x][y] = check

    def updateWumPus(self, x, y, check):
        self.W[x][y] = check
    
    def updateGold(self, x, y, check):
        if "G" in self.map_game[x][y]:
            self.G[x][y] = check
        
    
    def updateCurrentState(self,x,y):
        self.currentCave = {x,y}
        

    