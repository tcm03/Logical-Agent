import copy
from agentController import AgentController
from customParser import read_map, infer_information

def find_path(start,old,check_style,offset,direction,map_game,gameController):
    gameController.updatePerceiveAgent(start,map_game,old,check_style,direction)
    if gameController.checkAgentDie(start,check_style):
        path_find, point_path,fire,list_direction,grab,map_list, check = gameController.getReturnParameter()
        return path_find, point_path,fire,list_direction,grab,map_list, check
    path_can_go = gameController.getPathCanGo(start,check_style,offset,direction,old)
    if path_can_go[-1] == "StopUnsure":
        return path_can_go
    if path_can_go[-1] == "Stop":
        return path_can_go
    path_can_go_now = path_can_go[0]
    for step in path_can_go_now:
        path_find, point_path,fire,list_direction,grab,map_list, check = find_path((step[0], step[1]),start,step[2],step[3],step[4],step[5],gameController)
        if check == "Stop":
            return path_find,point_path,fire,list_direction,grab,map_list, "Stop"
        if check == "StopUnsure":
            return path_find,point_path,fire,list_direction,grab,map_list, "StopUnsure"


def getParameterUI(path_name,i):
    map_game = read_map(path_name)
    if map_game is None:
        return None
    world_map , start = infer_information(map_game)
    
    N = len(world_map) 
    start_position = start 
    old_position = (-1,-1) 
    check_style = 0 
    offset = None 
    direction = "right" 
    map_game_copy = copy.deepcopy(world_map) 
    
    gameController = AgentController(N,world_map,i)
    
    path_list, point_list,shoot_list,direction_list,grab_list,map_list, _ = find_path(start_position,old_position,check_style, offset,direction,map_game_copy,gameController)
    
    temp_n = len(path_list)
    temp_past_list = []
    temp_point_list = []
    temp_shoot_list = []
    temp_direction_list = []
    temp_grab_list = []
    temp_map_list = []
    
    action_list = []
    
    
    for i in range(temp_n):
        
        if shoot_list[i][0] != 1:
            if i == 0:
                action_list.append("Start")
            else:
                action_list.append("Forward")
            temp_past_list.append(path_list[i])
            temp_point_list.append(point_list[i])
            temp_shoot_list.append((0,0))
            temp_grab_list.append(0)
            temp_map_list.append(map_list[i])
            temp_direction_list.append(direction_list[i])
        
        
        if shoot_list[i][0] == 1:
            action_list.append("Shoot")
            temp_past_list.append(path_list[i])
            temp_point_list.append(point_list[i])
            temp_shoot_list.append(shoot_list[i])
            temp_grab_list.append(0)
            temp_map_list.append(copy.deepcopy(map_list[i]))
            temp_direction_list.append(direction_list[i])
        
        if grab_list[i] == 1:
            action_list.append("Grab")
            temp_past_list.append(path_list[i])
            temp_point_list.append(point_list[i])
            temp_shoot_list.append((0,0))
            temp_grab_list.append(grab_list[i])
            
            temp_direction_list.append(direction_list[i])
            if i < temp_n:
                for update_gold in range(i,temp_n):
                    x, y = path_list[i]
                    txt = map_list[update_gold][x][y]
                    if "G" in txt:
                        temp = txt[0:txt.index("G")]+txt[txt.index("G")+1:]
                    map_list[update_gold][x][y]=temp
                    if map_list[update_gold][x][y] == "":
                        map_list[update_gold][x][y]='-'
            temp_map_list.append(map_list[i])
        
        
        
        
        if i < temp_n -1:
            if direction_list[i] != direction_list[i+1]:
                if direction_list[i] == "left" and direction_list[i+1] == "right":
                    action_list.append(f"Turn {direction_list[i+1]}")
                    temp_past_list.append(path_list[i])
                    temp_point_list.append(point_list[i])
                    temp_shoot_list.append((0,0))
                    temp_grab_list.append(0)
                    temp_map_list.append(map_list[i])
                    temp_direction_list.append("up")
                    
                if direction_list[i] == "right" and direction_list[i+1] == "left":
                    action_list.append(f"Turn {direction_list[i+1]}")
                    temp_past_list.append(path_list[i])
                    temp_point_list.append(point_list[i])
                    temp_shoot_list.append((0,0))
                    temp_grab_list.append(0)
                    temp_map_list.append(map_list[i])
                    temp_direction_list.append("up")
                    
                if direction_list[i] == "up" and direction_list[i+1] == "down":
                    action_list.append(f"Turn left")
                    temp_past_list.append(path_list[i])
                    temp_point_list.append(point_list[i])
                    temp_shoot_list.append((0,0))
                    temp_grab_list.append(0)
                    temp_map_list.append(map_list[i])
                    temp_direction_list.append("left")
                    
                if direction_list[i] == "down" and direction_list[i+1] == "up":
                    action_list.append(f"Turn left")
                    temp_past_list.append(path_list[i])
                    temp_point_list.append(point_list[i])
                    temp_shoot_list.append((0,0))
                    temp_grab_list.append(0)
                    temp_map_list.append(map_list[i])
                    temp_direction_list.append("right")
                
                if direction_list[i] == "left" and direction_list[i+1] == "up":
                    action_list.append(f"Turn right")
                elif direction_list[i] == "right" and direction_list[i+1] == "up":
                    action_list.append(f"Turn left")
                elif direction_list[i] == "left" and direction_list[i+1] == "down":
                    action_list.append(f"Turn left")
                elif direction_list[i] == "right" and direction_list[i+1] == "down":
                    action_list.append(f"Turn right")
                elif direction_list[i] == "up" and direction_list[i+1] == "right":
                    action_list.append(f"Turn right")
                elif direction_list[i] == "down" and direction_list[i+1] == "left":
                    action_list.append(f"Turn right")
                elif direction_list[i+1] == "up" or direction_list[i+1] == "down":
                    action_list.append(f"Turn left")
                else:
                    action_list.append(f"Turn {direction_list[i+1]}")
                temp_past_list.append(path_list[i])
                temp_point_list.append(point_list[i])
                temp_shoot_list.append((0,0))
                temp_grab_list.append(0)
                temp_map_list.append(map_list[i])
                temp_direction_list.append(direction_list[i+1])
            
        if i == temp_n-1:
            action_list.append("Climb")
            temp_past_list.append(path_list[i])
            temp_point_list.append(point_list[i])
            temp_shoot_list.append((0,0))
            temp_grab_list.append(0)
            temp_map_list.append(map_list[i])
            temp_direction_list.append(direction_list[i])
            
    
    return temp_past_list, temp_point_list,temp_shoot_list,temp_direction_list,temp_grab_list,temp_map_list,action_list


def getParameter2(path_name):
    
    map_game = read_map(path_name)
    if map_game is None:
        return None
    N = len(map_game)
    best_past_list, best_point_list,best_shoot_list,best_direction_list,best_grab_list,best_map_list,best_action_list = getParameterUI(path_name,0)
    for i in range(1,N*N+1):
        try:  
            temp_past_list, temp_point_list,temp_shoot_list,temp_direction_list,temp_grab_list,temp_map_list,action_list = getParameterUI(path_name,i)
        except:
            continue
        if best_point_list[-1] < temp_point_list[-1]:
            best_past_list, best_point_list,best_shoot_list,best_direction_list,best_grab_list,best_map_list,best_action_list = temp_past_list, temp_point_list,temp_shoot_list,temp_direction_list,temp_grab_list,temp_map_list,action_list
            
    return best_past_list, best_point_list,best_shoot_list,best_direction_list,best_grab_list,best_map_list,best_action_list