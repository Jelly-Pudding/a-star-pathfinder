row = 7
column = 7

maze = [[0 for col in range(column)] for r in range(row)]

maze[4][4] = 1
maze[4][5] = 1
maze[4][6] = 1
maze[4][3] = 1


start_0 = 3
start_1 = 4

end_0 = 6
end_1 = 5

maze[start_0][start_1] = 3
maze[end_0][end_1] = 4

def printer(maze):
    for i in maze:
        print(i)

def find_start(maze):
    start = []
    for i in range(row):
        for j in range(column):
            if maze[i][j] == 3:
                start.append(i)
                start.append(j)
    return start

def find_end(maze):
    end = []
    for i in range(row):
        for j in range(column):
            if maze[i][j] == 4:
                end.append(i)
                end.append(j)
    return end

def find_adjacent_nodes(node):
    new_nodes_0 = []
    new_nodes_1 = []
    for i in range(8):
        if i < 3:
            new_nodes_0.append(node[0] - 1)
        elif i < 5:
            new_nodes_0.append(node[0])
        elif i < 8:
            new_nodes_0.append(node[0] + 1)
    for i in range(4):
        if i < 1:
            new_nodes_1.append(node[1] - 1)
            new_nodes_1.append(node[1])
            new_nodes_1.append(node[1] + 1)
        elif i < 2:
            new_nodes_1.append(node[1] - 1)
            new_nodes_1.append(node[1] + 1)
        elif i == 3:
            new_nodes_1.append(node[1] - 1)
            new_nodes_1.append(node[1])
            new_nodes_1.append(node[1] + 1)
    two_d = list(map(list, zip(new_nodes_0, new_nodes_1)))
    # if the index is greater than the row or column, it is converted to a negative number (so it can be dealt with afterwards)
    for i in range(len(two_d)):
        if two_d[i][0] >= row:
            two_d[i][0] = -1
        if two_d[i][1] >= column:
            two_d[i][1] = -1
    new_array = []
    # Removes all negative numbers from the two_d list. 
    for items in two_d:
        numbers = [x for x in items if x >= 0]
        try:
            if numbers[0] >= 0:
                new_array.append(numbers)
        except IndexError:
            pass
    remove_1_array = []
    #Removes coordinates if they equal to one in the maze. If there is only one coordinate because a negative number has been removed, there will be an Index Error (which will be ignored).
    for i in range(len(new_array)):
        try:
            index_one = new_array[i][0]
            index_two = new_array[i][1]
            if maze[index_one][index_two] != 1:
                remove_1_array.append(new_array[i])
            else:
                remove_1_array.pop(i)
        except IndexError:
            pass
    # If there is only one item in the list (i.e. if a negative number has been removed), the list is not included
    valid_coordinates = [x for x in remove_1_array if len(x) > 1]
    return valid_coordinates


def distance_till_end(node):
    distance = (node[0] - ending_node[0]) ** 2 + (node[1] - ending_node[1]) ** 2
    return distance

starting_node = find_start(maze)

ending_node = find_end(maze)

def a_star(starting_node):
    path = []
    open_list = []
    closed_list = []
    open_list.append({"the_node": starting_node, "g_value": 0, "f_value": 0})
    while True:
        print(open_list)
        #deals with the current node
        dict_with_lowest_f_value = min(open_list, key=lambda x:x["f_value"])
        current_node = dict_with_lowest_f_value["the_node"]  
        current_node_index = next((index for (index, d) in enumerate(open_list) if d["the_node"] == current_node), None)
        closed_list.append(open_list[current_node_index])
        open_list.pop(current_node_index)
        
        #found goal
        
        path.append(current_node)
        if current_node == ending_node:
            return path

        #generate child nodes
        children = find_adjacent_nodes(current_node)
        
        for child in children:
            #if the child is not in the closed list
            if not any(d['the_node'] == child for d in closed_list):
                closed_current_node_index = next((index for (index, d) in enumerate(closed_list) if d["the_node"] == current_node), None)
                child_dist_from_start = closed_list[closed_current_node_index]["g_value"] + 1
                child_dist_from_end = distance_till_end(child)
                child_f = child_dist_from_start + child_dist_from_end

                
                #Checks if the child is in the open list
                if any(d['the_node'] == child for d in open_list):
                    child_index = next((index for (index, d) in enumerate(open_list) if d["the_node"] == child), None)
                    open_list_dist_value_from_start = open_list[child_index]["g_value"]
                #compares child's new distance with the value from the open_list 
                try:
                    if child_dist_from_start > open_list_dist_value_from_start:
                        open_list[child_index]["g_value"] = child_dist_from_start
                        open_list[child_index]["f_value"] = child_f
                        open_list_dist_value_from_start = None
                #Errors will occur if the child was not in the open list 
                except Exception:
                    open_list.append({"the_node": child, "g_value": child_dist_from_start, "f_value": child_f})

try:
    print(a_star(starting_node))
except ValueError:
    print("There is no solution")

printer(maze)
