import copy
from agent import Agent

map_game = [
                 ['S','S','S','SG'], # Rooms [1,1] to [4,1]
                 ['W','W','W','W'], # Rooms [1,2] to [4,2] 
                 ['S','S','S','S'], # Rooms [1,3] to [4,3]
                 ['-','-','-','-'], # Rooms [1,4] to [4,4]
]

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

agent = Agent(0,0,4,map_game)
path, point,shoot,direction,grab, check = agent.find_path((0,0),(-1,-1),0, None,"right")
# path = agent.find_path_to_exit((0,0),(3,3))

# print(path) : danh sách các bước đi của agent
# print(point): điểm hiện tại của agent tương ứng với tường bước đi
# print(shoot): agent có bắn mũi tên tại vị trí đó hay không(0: không bắn, 1: có bắn)
# print(direction): hướng hiện tại của agent(right left top down)
# print(grab): (agent có nhặt vàng tại vị trí đó hay không)
# print(len(path))
# print(len(point))
# print(len(shoot))
# print(len(direction))
# print(len(grab))

# print("--------------")
# print(agent.P)
# print(agent.W)
# print(agent.knowledgePit)
# print(agent.knowledgeWum)



# map_game1 = copy.deepcopy(map_game)
# print(map_game1)

