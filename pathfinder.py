import ast
import numpy as np
row = 7
column = 7

maze = [[0 for col in range(column)] for r in range(row)]

start_0 = 0
start_1 = 0

end_0 = 6
end_1 = 6

maze[1][1] = 1
maze[1][2] = 1
maze[1][0] = 1
maze[1][3] = 1
maze[1][4] = 1
maze[1][5] = 1
maze[2][6] = 1
maze[3][6] = 1
maze[3][5] = 1
maze[3][4] = 1

maze[start_0][start_1] = 3
maze[end_0][end_1] = 4

'''
maze[0][0] = 1
maze[1][0] = 1
maze[1][1] = 1

maze[2][0] = 1
maze[2][1] = 1
maze[2][2] = 1
maze[2][3] = 1
maze[3][3] = 1


start_0 = 4
start_1 = 0

end_0 = 0
end_1 = 4

maze[start_0][start_1] = 3
maze[end_0][end_1] = 4

'''

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
    return sum(abs(val1-val2) for val1, val2 in zip(node, ending_node))

starting_node = find_start(maze)

ending_node = find_end(maze)



def a_star(starting_node):
    child_count = 0 
    count = 0
    path = []
    unseen_list = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            unseen_list.append({"the_node": [i, j]})
    print(unseen_list)
    open_list = []
    closed_list = []
    open_list.append({"the_node": starting_node, "parent": None, "g_value": 0, "f_value": 0})
    count = 0
    while open_list != []:
        count += 1
        print(count)
        #deals with the current node
        dict_with_lowest_f_value = min(open_list, key=lambda x:x["f_value"])
        current_node = dict_with_lowest_f_value["the_node"]
        parent_of_current_node = dict_with_lowest_f_value["parent"]
        current_node_g_value = dict_with_lowest_f_value["g_value"]  
        current_node_index = next((index for (index, d) in enumerate(open_list) if d["the_node"] == current_node), None)
        print("open_list before pop: " + str(open_list))
        open_list.pop(current_node_index)

        print("open_list after pop: " + str(open_list))



        children = find_adjacent_nodes(current_node)
        for child in children:
            parent = current_node
            closed_current_node_index = next((index for (index, d) in enumerate(closed_list) if d["the_node"] == current_node), None)
            child_dist_from_start = current_node_g_value + 1
            child_dist_from_end = distance_till_end(child)
            child_f = child_dist_from_start + child_dist_from_end
            print(str(child) + " g = " + str(child_dist_from_start) + " h = " + str(child_dist_from_end) + " f = " + str(child_f))

            if child == ending_node:
                print("\n")
                print("open " + str(open_list) + "\n")
                print("closed " + str(closed_list))
                print("parent of current node:" + str(parent_of_current_node))
                path = []
                path.append(child)
                path.append(parent)
                parent = parent_of_current_node
                while parent != None:
                    path.append(parent)
                    parent_closed_list_index = next((index for (index, d) in enumerate(closed_list) if d["the_node"] == parent), None)
                    if parent_closed_list_index == None:
                        parent = None
                    else:
                        parent = closed_list[parent_closed_list_index]["parent"]
                return path[::-1]


            #equals None if the child node is not in the open list - else gives the index of the dictionary's place in the list
            child_open_list_node_index = next((index for (index, d) in enumerate(open_list) if d["the_node"] == child), None)
            if child_open_list_node_index != None:
                if open_list[child_open_list_node_index]["f_value"] < child_f:
                    continue
            
            child_closed_list_node_index = next((index for (index, d) in enumerate(closed_list) if d["the_node"] == child), None)
            if child_closed_list_node_index != None:
                if closed_list[child_closed_list_node_index]["f_value"] < child_f:
                    continue
                else:
                    if child_open_list_node_index != None:
                        open_list[child_open_list_node_index] = {"the_node": child, "parent": parent, "g_value": child_dist_from_start, "f_value": child_f}

            child_unseen_list_node_index = next((index for (index, d) in enumerate(unseen_list) if d["the_node"] == child), None)
            if child_unseen_list_node_index != None:
                open_list.append({"the_node": child, "parent": parent, "g_value": child_dist_from_start, "f_value": child_f})
                unseen_list.pop(child_unseen_list_node_index)

        closed_list.append(dict_with_lowest_f_value)

        print("closed list at end of while loop: " + str(closed_list))
        print("open list at end of while loop: " + str(open_list))
            
            

            
        
def main():
    try:
        path = a_star(starting_node)

    except ValueError:
        print("There is no solution")


    printer(maze)

    print(path)

if __name__ == "__main__":
    main()
else:
    pass
