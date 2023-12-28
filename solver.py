import copy
from agentController import AgentController
from customparser import read_map, infer_information

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


def getParameterUI(path_name):
    map_game = read_map(path_name)
    if map_game is None:
        return None
    world_map , start = infer_information(map_game)
    N = len(world_map) # kích thước mảng khi đọc vào
    start_position = start # vị trí bắt đầu của agent trong map
    old_position = (-1,-1) # vị trí trước khi đi đến ô bắt đầu (mặc định khi khởi tạo luôn là (-1,-1))
    check_style = 0 # có 0,1,2( 0: ô bình thường an toàn không xét, 1 ô xét bắn cung, 2: ô nghi ngờ không chắc chắn)  )
    offset = None # moves vừa mới đi (0,1) (0,-1) (1,0) (-1,0) để xét trường hợp quay lui khi không có ô nào để đi
    direction = "right" # hướng đi mặc định ban đầu luôn luôn là right. Ngoài ra còn có left, up, down
    map_game_copy = copy.deepcopy(world_map) # mảng ban đầu truyền vào sau khi đọc (mục đích để lưu phục vụ vẽ UI)

    gameController = AgentController(N,world_map)
    
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
        
        
        if grab_list[i] == 1:
            action_list.append("Grab")
            temp_past_list.append(path_list[i])
            temp_point_list.append(point_list[i])
            temp_shoot_list.append((0,0))
            temp_grab_list.append(grab_list[i])
            temp_map_list.append(map_list[i])
            temp_direction_list.append(direction_list[i])
        
        if i < temp_n -1:
            if direction_list[i] != direction_list[i+1]:
                action_list.append(f"Turn {direction_list[i+1]}")
                temp_past_list.append(path_list[i])
                temp_point_list.append(point_list[i])
                temp_shoot_list.append((0,0))
                temp_grab_list.append(0)
                temp_map_list.append(map_list[i])
                temp_direction_list.append(direction_list[i+1])
            
        if shoot_list[i][0] == 1:
            action_list.append("Shoot")
            temp_past_list.append(path_list[i])
            temp_point_list.append(point_list[i])
            temp_shoot_list.append(shoot_list[i])
            temp_grab_list.append(0)
            temp_map_list.append(map_list[i])
            temp_direction_list.append(direction_list[i])
            
        if i == temp_n-1:
            action_list.append("Climb")
            temp_past_list.append(path_list[i])
            temp_point_list.append(point_list[i])
            temp_shoot_list.append((0,0))
            temp_grab_list.append(0)
            temp_map_list.append(map_list[i])
            temp_direction_list.append(direction_list[i])
            
    
    return temp_past_list, temp_point_list,temp_shoot_list,temp_direction_list,temp_grab_list,temp_map_list