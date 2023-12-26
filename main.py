import copy
from agentController import AgentController
from solver import find_path, getParameterUI


# map_game = [
#                  ['S','S','S','SG'], # Rooms [1,1] to [4,1]
#                  ['WS','WS','WS','WS'], # Rooms [1,2] to [4,2] 
#                  ['S','S','S','S'], # Rooms [1,3] to [4,3]
#                  ['-','-','-','-'], # Rooms [1,4] to [4,4]
# ]


# map_game = [
#                  ['S','B','S','BG'], # Rooms [1,1] to [4,1]
#                  ['WB','PS','BW','SP'], # Rooms [1,2] to [4,2] 
#                  ['S','B','S','B'], # Rooms [1,3] to [4,3]
#                  ['-','-','-','-'], # Rooms [1,4] to [4,4]
# ]

# map_game = [
#                  ['-','B','P','B'], # Rooms [1,1] to [4,1]
#                  ['S','-','B','-'], # Rooms [1,2] to [4,2] 
#                  ['W','S','-','G'], # Rooms [1,3] to [4,3]
#                  ['S','-','G','G'], # Rooms [1,4] to [4,4]
#                 ]


# map_game = [
#                  ['-','B','P','B'], # Rooms [1,1] to [4,1]
#                  ['S','-','B','-'], # Rooms [1,2] to [4,2] 
#                  ['W','S','B','-'], # Rooms [1,3] to [4,3]
#                  ['S','B','P','BG'], # Rooms [1,4] to [4,4]
#                 ]

"""
# Map hợp lệ khi đã cập nhật breeze và squeeze(Lưu ý map_game ở dưới là hợp lệ, trong khi map_game1
# chưa cập nhât squeeze tại W). Mỗi ô nếu có cập nhật squeeze và brezze chỉ cập nhật 1 S hoặc 1B)
"""
# map_game = [['B', 'S', 'WS', 'S'], ['P', 'BS', 'WS', 'S'], ['B', '-', 'S', '-'], ['A', '-', '-', '-']]

# map_game1 = [
#                  ['B', 'S', 'W', 'S'], # Rooms [1,1] to [4,1]
#                  ['P', 'SB', 'W', 'S'], # Rooms [1,2] to [4,2] 
#                  ['B', '-', 'S', '-'], # Rooms [1,3] to [4,3]
#                  ['-', '-', '-', '-'], # Rooms [1,4] to [4,4]
#                 ]

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

# print(len(shoot))

path_list, point_list,shoot_list,direction_list,grab_list,map_list = getParameterUI("test_input.txt")
print(path_list)
print(point_list)
print(shoot_list)
print(direction_list)
print(grab_list)
print(map_list)

print(len(path_list))
print(len(point_list))
print(len(shoot_list))
print(len(direction_list))
print(len(grab_list))
print(len(map_list))