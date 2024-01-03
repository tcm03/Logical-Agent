import copy
from agentController import AgentController
from solver import find_path, getParameterUI

















world_map = [['PB', 'PB', 'PB', 'PB'], ['GBS', 'GBS', 'PBS', 'GB'], ['WS', 'WS', 'WBS', 'S'], ['AS', 'S', 'S', 'G']]

"""
# Map hợp lệ khi đã cập nhật breeze và squeeze(Lưu ý map_game ở dưới là hợp lệ, trong khi map_game1
# chưa cập nhât squeeze tại W). Mỗi ô nếu có cập nhật squeeze và brezze chỉ cập nhật 1 S hoặc 1B)
"""

# map_game = [['B', 'S', 'WS', 'S'], 
#             ['P', 'BS', 'WS', 'S'], 
#             ['B', '-', 'S', '-'], 
#             ['-', '-', '-', '-']]
# map_game = [
# ['B', 'S', 'WS', 'S', 'B', 'S', 'WS', 'S', 'WS', 'S'],
# ['P', 'BS', 'WS', 'SB', 'PB', 'BS', 'WS', 'S', 'WS', 'S'],
# ['B', '-', 'S', 'B', 'PB', 'BS', 'WS', 'S', 'WS', 'S'],
# ['-', '-', '-', '-', 'B', '-', 'S', '-', 'S', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
# ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]

# map_game1 = [
#                  ['B', 'S', 'W', 'S'], # Rooms [1,1] to [4,1]
#                  ['P', 'SB', 'W', 'S'], # Rooms [1,2] to [4,2] 
#                  ['B', '-', 'S', '-'], # Rooms [1,3] to [4,3]
#                  ['-', '-', '-', '-'], # Rooms [1,4] to [4,4]
#                 ]

# map_game = [['B', 'GS', 'WS', 'S'], 
#             ['P', 'BS', 'WS', 'S'], 
#             ['B', '-', 'S', '-'], 
#             ['-', '-', '-', '-']]

# N = 4 # kích thước mảng khi đọc vào
# start_position = (3,0) # vị trí bắt đầu của agent trong map
# old_position = (-1,-1) # vị trí trước khi đi đến ô bắt đầu (mặc định khi khởi tạo luôn là (-1,-1))
# check_style = 0 # có 0,1,2( 0: ô bình thường an toàn không xét, 1 ô xét bắn cung, 2: ô nghi ngờ không chắc chắn)  )
# offset = None # moves vừa mới đi (0,1) (0,-1) (1,0) (-1,0) để xét trường hợp quay lui khi không có ô nào để đi
# direction = "right" # hướng đi mặc định ban đầu luôn luôn là right. Ngoài ra còn có left, up, down
# map_game_copy = copy.deepcopy(map_game) # mảng ban đầu truyền vào sau khi đọc (mục đích để lưu phục vụ vẽ UI)

# gameController = AgentController(N,map_game)
# path, point,shoot,direction,grab,map_list, check = find_path(start_position,old_position,check_style, offset,direction,map_game_copy,gameController)

# print(path)  #danh sách các bước đi của agent. Bước đi cuối cùng khi vẽ UI nên check thử có trùng với vị trí exit không nếu có thì nghĩa là đã climb ngược lại thì không.
# if path[-1] == (N-1,0):
#     print("Climb")
# else:
#     print("Not climb")
# print(point) #điểm hiện tại của agent tương ứng với tường bước đi. Điểm đã được tính từ vị trí đầu đến cuối nên không cần xử lý thêm
# print(shoot) #agent có bắn mũi tên tại vị trí đó hay không(0: không bắn, 1: có bắn). Nếu bắn cung thì tại vị trí đó path sẽ có hiện ô tiếp theo nó đi nhưng chưa di chuyển qua.
# print(direction) #hướng hiện tại của agent (right left top down)
# print(grab) #agent có nhặt vàng tại vị trí đó hay không (0: là không nhặt, 1 là có nhặt)
# print(map_list) # danh sách các map tại từng bước của agent. Mỗi map kết hợp với các mảng trên để xét perceive của mỗi ô agent đang đứng
# print(check) # gồm Stop, StopUnsure. Nếu là Stop thì agent đã chết hoặc leo ra khỏi map. Ngược lại thì agent dừng vì 4 ô xung quang nó đều nguy hiểm nên không tiến hành đi nữa 

# map_game = 

N = len(world_map) # kích thước mảng khi đọc vào
start_position = (3,0) # vị trí bắt đầu của agent trong map
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
    
    if grab_list[i] == 1:
        action_list.append("Grab")
        temp_past_list.append(path_list[i])
        temp_point_list.append(point_list[i])
        temp_shoot_list.append((0,0))
        temp_grab_list.append(grab_list[i])
        temp_map_list.append(map_list[i])
        temp_direction_list.append(direction_list[i])
        if i+1 < temp_n:
            for update_gold in range(i+1,temp_n):
                x, y = path_list[i]
                txt = map_list[update_gold][x][y]
                if "G" in txt:
                    temp = txt[0:txt.index("G")]+txt[txt.index("G")+1:]
                map_list[update_gold][x][y]=temp
                if map_list[update_gold][x][y] == "":
                    map_list[update_gold][x][y]='-'
    
    if shoot_list[i][0] == 1:
        action_list.append("Shoot")
        temp_past_list.append(path_list[i])
        temp_point_list.append(point_list[i])
        temp_shoot_list.append(shoot_list[i])
        temp_grab_list.append(0)
        temp_map_list.append(map_list[i])
        temp_direction_list.append(direction_list[i])
    
    
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
        
print(temp_past_list)
print(temp_point_list)