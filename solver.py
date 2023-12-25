

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
            