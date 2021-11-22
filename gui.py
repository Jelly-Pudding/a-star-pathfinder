import pygame
import numpy as np
import time
import sys

# Default size of row and column if the user does not provide input

num_of_rows = 10
num_of_cols = 10

# This window will ask for user input (row size and column size)

pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.font.init()
pygame.display.set_caption("Select Size")
myfont = pygame.font.SysFont("timesnewroman", 30)
input_box1 = pygame.Rect(30, 45, 150, 32)
input_box2 = pygame.Rect(30, 115, 150, 32)
done_box = pygame.Rect(50, 160, 110, 25)
color_inactive = pygame.Color("lightskyblue3")
# Color when the player clicks on the box
color_active = pygame.Color("dodgerblue2")
active1 = False
active2 = False
input_text = ""
input_text2 = ""

def displayer():
    textsurface = myfont.render("Enter Column#:", False, (90, 0, 0))
    screen.blit(textsurface,(7,10))
    secondquestion = myfont.render("Enter Row#:", False, (90, 0, 0))
    screen.blit(secondquestion,(30,80))
    if active1 == True:
        pygame.draw.rect(screen, color_active, input_box1)
    else:
        pygame.draw.rect(screen, color_inactive, input_box1)
    if active2 == True:
        pygame.draw.rect(screen, color_active, input_box2)
    else:
        pygame.draw.rect(screen, color_inactive, input_box2)        
    create_input_text_1 = myfont.render(input_text, True, (50, 0, 0))
    screen.blit(create_input_text_1, (39,43))
    create_input_text_2 = myfont.render(input_text2, True, (50, 0, 0))
    screen.blit(create_input_text_2, (39, 115))

    pygame.draw.rect(screen, (100, 100, 100), done_box)
    finish_text = myfont.render("Done", True, (100, 0, 0))
    screen.blit(finish_text, (73, 155))
    pygame.display.update()

running = True
  
while running:  
    displayer()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box1.collidepoint(event.pos):
                active1 = not active1
            else:
                active1 = False
            color = color_active if active1 else color_inactive
            if input_box2.collidepoint(event.pos):
                active2 = not active1
            else:
                active2 = False
            color = color_active if active2 else color_inactive
            if done_box.collidepoint(event.pos):
                pygame.quit()
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                running = False
            if active1 == True:
                active2 = False
                if event.key == pygame.K_RETURN:
                    num_of_rows = input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    num_of_rows = input_text
                else:
                    input_text += event.unicode
                    num_of_rows = input_text
            if active2 == True:
                active1 = False
                if event.key == pygame.K_RETURN:
                    num_of_cols = input_text2
                elif event.key == pygame.K_BACKSPACE:
                    input_text2 = input_text2[:-1]
                    num_of_cols = input_text2
                else:
                    input_text2 += event.unicode
                    num_of_cols = input_text2

try:
    num_of_rows = int(num_of_rows)
    num_of_cols = int(num_of_cols)
except ValueError:
    # If invalid input is given, these default values will be used
    num_of_rows = 10
    num_of_cols = 10
# print(num_of_rows)
# print(num_of_cols)

maze = [[0 for col in range(num_of_cols)] for row in range(num_of_rows)]

# A simple function that allows one to view the maze in console

def printer(maze):
    for i in maze:
        print(i)


# printer(maze)

# This new window will be the actual maze game the user plays

pygame.init()

pygame.display.set_caption("Maze")

# Each box (or node) will be 20x20. Therefore, width (number of rows) and height (number of columns) are multiplied by 20 so there is the exact amount of space needed for every box

screen = pygame.display.set_mode((num_of_rows * 20, num_of_cols * 20))


# If the enter key is pressed, then the a* algorithm starts and this variable becomes True

hit_enter = False

# A function that displays the maze as a grid with coloured boxes. This will be called after the find_adjacent_nodes function and the a* function (which are located below
# this game_display function).

def game_display():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            # The starting node (shown as blue)
            if maze[i][j] == 3:
                pygame.draw.rect(screen, (0,0,255), pygame.Rect(20*i, 20*j, 20, 20))
            # The ending node (shown as green)
            elif maze[i][j] == 4:
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(20*i, 20*j, 20, 20))
            # Barriers in the path (shown as red)
            elif maze[i][j] == 1:
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(20*i, 20*j, 20, 20)) 
            # Normal nodes (shown as grey)        
            else:
                pygame.draw.rect(screen, (40,40,40), pygame.Rect(20*i, 20*j, 20, 20))

    # If the user clicks after they have seen the algorithm finish the maze, then the path the algorithm found is removed from the gui
    # (due to the bool variable "remove_fastest_path_after_clicking")

    if hit_enter == True and remove_fastest_path_after_clicking == False:
        for items in best_path:
            pygame.draw.rect(screen, (0,255,0), pygame.Rect(20*items[1], 20*items[0], 20, 20))

    # Lines to separate the boxes from one another

    for i in range(len(maze)):
        pygame.draw.line(screen, (255, 255, 255), (i*20, 0), (i*20, num_of_cols*20), 2)
        for j in range(len(maze[i])):
            pygame.draw.line(screen, (255, 255, 255), (0, j*20), (num_of_rows*20, j*20), 2)

    # Line across the bottom

    pygame.draw.line(screen, (255, 255, 255), (0, num_of_cols*20), (num_of_rows*20, num_of_cols*20), 4)

    # Line down the right hand side

    pygame.draw.line(screen, (255, 255, 255), (num_of_rows*20, 0), (num_of_rows*20, num_of_cols*20), 4)

    pygame.display.update()

# A function that returns the nodes that are connected to whatever node gets inputted into the function. These connections can be vertical, horizontal, and diagonal.

def find_adjacent_nodes(node):
    new_nodes_0 = []
    new_nodes_1 = []
    # Iteratively gets indices from all the adjacent nodes (8 in total). The index of the current row and column will only appear in the list twice 
    # (because the node inputted into the function does not really count as an adjacent node).
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
    two_d = []
    two_d = list(map(list, zip(new_nodes_0, new_nodes_1)))
    # If the index is greater than the size of the row or the column, it is converted to a negative number (so it can be dealt with afterwards)
    for i in range(len(two_d)):
        if two_d[i][0] >= num_of_cols:
            two_d[i][0] = -1
        if two_d[i][1] >= num_of_rows:
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
    # Removes coordinates if they equal to one in the maze. If there is only one coordinate because a negative number has been removed, there will be 
    # an Index Error (which will be ignored).
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
    # If there is only one item in the list (i.e. if a negative number has been removed), the coordinates of the (invalid) adjacent node are not included.
    valid_coordinates = [x for x in remove_1_array if len(x) > 1]
    return valid_coordinates

# These distance functions can estimate the distance from any node in the maze to the ending node.

def manhattan_distance(node):
    h = abs(node[0] - ending_node[0]) + abs(node[1] - ending_node[1])
    return h

def diagonal_distance(node):
    dx = abs(node[0] - ending_node[0])
    dy = abs(node[1] - ending_node[1])
    # Assumes length of nodes is 1, and thus the diagonal distance between nodes is the square root of 2.
    # These numbers are multiplied by 10 to give 10 and 14.
    h = 10 * (dx + dy) + (14 - 2 * 10) * min(dx, dy)
    h = h - 4
    return h

def euclidean_distance(node):
    node_numpy = np.array(node)
    ending_node_numpy = np.array(ending_node)
    return np.linalg.norm(node_numpy - ending_node_numpy)

def zero_distance(node):
    return 0


# When this is set to True, the a* function will show the algorithm trying out different paths to the end node.
show_algorithm_in_progress = False

def a_star(starting_node, distance_till_end_function):
    #child_count = 0 
    #count = 0
    # A list that will store the path the algorithm found
    path = []
    # The open list contains candidate nodes that will be compared with one another (and the one with the lowest f value
    # will be the one that gets picked)
    open_list = []
    # The closed list tracks the nodes that were picked as having the lowest f value. This will prove useful when it comes to
    # finding the path the algorithm found through backtracking
    closed_list = []
    # The first node that will be considered is the starting node (which the user themselves will pick)
    # Both the open and closed lists will contain dictionaries so the information from each node (parent node and the relevant distance values) can be easily retrived.
    # The parent for the starting_node is set to None so that, when backtracking, we know the starting node has been reached (and hence there is no
    # need to continue trying to backtrack)
    open_list.append({"the_node": starting_node, "parent": None, "g_value": 0, "f_value": 0})
    while open_list != []:
        #count += 1
        #print(count)
        # Finds the dictionary in the open list with the lowest f value (which is the distance from the starting node plus the estimated distance to the ending node)
        dict_with_lowest_f_value = min(open_list, key=lambda x:x["f_value"])
        current_node = dict_with_lowest_f_value["the_node"]
        parent_of_current_node = dict_with_lowest_f_value["parent"]
        current_node_g_value = dict_with_lowest_f_value["g_value"]  
        # Equals None if the current node is not in the open list - otherwise this gives the index of the dictionary's place in the list.
        # It will never equal None because the current node just came from the open list, but this syntax works and it will be used throughout
        # this function.
        current_node_index = next((index for (index, d) in enumerate(open_list) if d["the_node"] == current_node), None)
        #print("open_list before pop: " + str(open_list))
        # Because we will now consider the node found in the open list, it is removed from the open list (so we won't consider it again / get stuck in a loop 
        # if it always has the lowest f value in the list)
        open_list.pop(current_node_index)
        #print("open_list after pop: " + str(open_list))
        children = find_adjacent_nodes(current_node)
        for child in children:
            parent = current_node
            # As the child is one square away from its parent, its distance from the start can be found by simping adding one on top of
            # the parent's distance from the starting node. This distance won't necessarily be the quickest route to get from the starting
            # node to the child node. 
            child_dist_from_start = current_node_g_value + 1
            child_dist_from_end = distance_till_end_function(child)
            child_f = child_dist_from_start + child_dist_from_end
            # We have found our optimum solution if the below line is true, so the algorithm ends and the quickest route is found through backtracking. 
            if child == ending_node:
                #print("\n")
                #print("open " + str(open_list) + "\n")
                #print("closed " + str(closed_list))
                #print("parent of current node:" + str(parent_of_current_node))
                path.append(child)
                path.append(parent)
                parent = parent_of_current_node
                # The parent of starting_node is None, and so this while loop will backtrack until we reach the starting node
                while parent != None:
                    path.append(parent)
                    parent_closed_list_index = next((index for (index, d) in enumerate(closed_list) if d["the_node"] == parent), None)
                    if parent_closed_list_index == None:
                        parent = None
                    else:
                        parent = closed_list[parent_closed_list_index]["parent"]
                # The path list is reversed to give the path from the starting node to the ending node 
                return path[::-1]


            # Equals None if the child node is not in the open list - otherwise this gives the index of the dictionary's place in the list
            child_open_list_node_index = next((index for (index, d) in enumerate(open_list) if d["the_node"] == child), None)
            if child_open_list_node_index != None:
                # Because the child's f_value is greater than the value it has in the open list, this current child of the iteration will be skipped.
                if open_list[child_open_list_node_index]["f_value"] < child_f:
                    continue
                else:
                    open_list[child_open_list_node_index] = {"the_node": child, "parent": parent, "g_value": child_dist_from_start, "f_value": child_f}
            
            child_closed_list_node_index = next((index for (index, d) in enumerate(closed_list) if d["the_node"] == child), None)
            # If it's not in the open list, and if it's not in the closed list (or if it is and it beats the closed list's value), then this node will need
            # to be considered and so it is appended to the open list
            if child_open_list_node_index == None:
                if child_closed_list_node_index == None or closed_list[child_closed_list_node_index]["f_value"] > child_f:
                    open_list.append({"the_node": child, "parent": parent, "g_value": child_dist_from_start, "f_value": child_f})
            if child_closed_list_node_index != None:
                # For similar reasoning, because the closed list has the node having a lower f_value, the child gets skipped. 
                if closed_list[child_closed_list_node_index]["f_value"] < child_f:
                    continue
                else:
                    # To get to this line, the child's f_value is worthwhile recording. The original dictionary values for the node are overwritten
                    # by the new set of values.  
                    closed_list[child_closed_list_node_index] = {"the_node": child, "parent": parent, "g_value": child_dist_from_start, "f_value": child_f}
                    # Also update the open list values for good measure (if it is in the open list)
                    if child_open_list_node_index != None:
                        open_list[child_open_list_node_index] = {"the_node": child, "parent": parent, "g_value": child_dist_from_start, "f_value": child_f}
        # This bool variable decides whether or not the algorithm's progress and outcome are shown on the gui board.

        if show_algorithm_in_progress == True:
            # The bool variable bruteforce_dijkstra will be True when the a* path finding algorithm failed to find the optimal path due to 
            # overestimating the distance to the end node. Because the alternative method (dijkstra) is much slower, there won't be any time delay whatsoever 
            # if this variable is True. 
            # Furthermore, for smaller board configurations, the output to the gui board will be slowed down (otherwise it's over in the blink of an eye)
            if num_of_cols + num_of_rows <= 20 and bruteforce_dijkstra != True:
                time.sleep(0.05)
            elif num_of_cols + num_of_rows <= 30 and bruteforce_dijkstra != True:
                time.sleep(0.02)
            elif num_of_cols + num_of_rows <= 40 and bruteforce_dijkstra != True:
                time.sleep(0.01)
            # The child nodes are coloured pink
            for child in children:
                pygame.draw.rect(screen, (255,192,203), pygame.Rect(20*child[1], 20*child[0], 20, 20))
            for items in closed_list:
                # The nodes in closed_list appear as dark blue
                pygame.draw.rect(screen, (114,192,203), pygame.Rect(20*items["the_node"][1], 20*items["the_node"][0], 20, 20))  
            current_fastest_path = []
            current_fastest_path.append(current_node)
            parent = parent_of_current_node
            while parent != None:
                current_fastest_path.append(parent)
                parent_closed_list_index = next((index for (index, d) in enumerate(closed_list) if d["the_node"] == parent), None)
                if parent_closed_list_index == None:
                    parent = None
                else:
                    parent = closed_list[parent_closed_list_index]["parent"]
            # The nodes in the current fastest path appear as light blue (to contrast the nodes in the closed list)
            for items in current_fastest_path:
                pygame.draw.rect(screen, (150,255,220), pygame.Rect(20*items[1], 20*items[0], 20, 20))
            for i in range(len(maze)):
                pygame.draw.line(screen, (255, 255, 255), (i*20, 0), (i*20, num_of_cols*20), 2)
                for j in range(len(maze[i])):
                    pygame.draw.line(screen, (255, 255, 255), (0, i*20), (num_of_rows*20, i*20), 2)
            if num_of_rows > num_of_cols:
                # When the number of rows is greater, this will fill the lines in the columns that won't otherwise be covered
                length_one = len(maze) 
                length_two = len(maze[0])
                difference_of_length = length_two - length_one
                from_the_end = num_of_rows - difference_of_length
                for i in range(difference_of_length):
                    pygame.draw.line(screen, (255, 255, 255), (from_the_end*20, 0), (from_the_end*20, from_the_end*20), 2)
                    from_the_end += 1
            # Line across the bottom
            pygame.draw.line(screen, (255, 255, 255), (0, num_of_cols*20), (num_of_rows*20, num_of_cols*20), 4)
            # Line down the right hand side
            pygame.draw.line(screen, (255, 255, 255), (num_of_rows*20, 0), (num_of_rows*20, num_of_cols*20), 4)
            pygame.display.update()
            # End of the gui display
            
        # The node that was being considered has now been considered, so it is added to the closed list.
        closed_list.append(dict_with_lowest_f_value)
        #print("closed list at end of while loop: " + str(closed_list))
        #print("open list at end of while loop: " + str(open_list))


#3 represents the starting node, and #4 the ending node (or goal node). Each should only be placed once, so these bool variables keep track of whether they have been placed.

three_used_up = False
four_used_up = False

# if a* does not find the quickest path (due to overestimating the distance to the end node) then the distance function which always returns 0 will produce the shorest path
# to the destination. Because this is a much longer method for arriving at the destination, this variable will be set to true so that when one sees the grid gui, there will be
# no time delay. 

bruteforce_dijkstra = False

remove_fastest_path_after_clicking = False

#This list places the positioning of every box on the screen in a unique dictionary, and the dictionaries also store where
#the corresponding node will be in the maze list (referred to in the dictionary's key as "coordinates")

input_box_list = []
for i in range(len(maze)):
    for j in range(len(maze[i])):
        input_box_list.append({"rectangle": pygame.Rect(20*i, 20*j, 20, 20), "coordinates": [i, j]})

running = True

while running:
    game_display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_r:
                for i in range(len(maze)):
                    for j in range(len(maze[i])):
                        maze[i][j] = 0
                three_used_up = False
                four_used_up = False
                bruteforce_dijkstra = False
                enter_key_counter = 0
                remove_fastest_path_after_clicking = True
                show_algorithm_in_progress = False
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                remove_fastest_path_after_clicking = False
                # A variable that makes sure only the fastest path is shown (e.g. the path that used the manhattan distance etc.)
                show_algorithm_in_progress = False
                # Resets the maze (removes the fastest path marked in green and shows the starting and ending nodes again)
                for i in range(len(maze)):
                    for j in range(len(maze[i])):
                        # The starting node (shown as blue)
                        if maze[i][j] == 3:
                            pygame.draw.rect(screen, (0,0,255), pygame.Rect(20*i, 20*j, 20, 20))
                        # The ending node (shown as green)
                        elif maze[i][j] == 4:
                            pygame.draw.rect(screen, (0,255,0), pygame.Rect(20*i, 20*j, 20, 20))
                        # Barriers in the path (shown as red)
                        elif maze[i][j] == 1:
                            pygame.draw.rect(screen, (255,0,0), pygame.Rect(20*i, 20*j, 20, 20)) 
                            # "Normal" nodes (shown as grey)
                        else:
                            pygame.draw.rect(screen, (40,40,40), pygame.Rect(20*i, 20*j, 20, 20))
                maze = np.array(maze)
                maze = np.swapaxes(maze,0,1)
                #print("adjacent nodes = " + str(find_adjacent_nodes([0, 3])))
                #print(maze)
                # There will be a TypeError if the maze is impossible to complete
                # (For example if barrier blocks surround the exit)
                try:
                    path_diagonal = a_star(starting_node, diagonal_distance)
                    path_manhattan = a_star(starting_node, manhattan_distance)                   
                    path_euclidean = a_star(starting_node, euclidean_distance)
                    path_zero = a_star(starting_node, zero_distance)
                    printer(maze)
                    # prevents "Diagonal path: None" being printed to the console if there is no solution
                    if path_diagonal != None:
                        print("Diagonal path: " + str(path_diagonal))
                    print("Diagonal path length: " + str(len(path_diagonal)))
                    print("Manhattan path: " + str(path_manhattan))
                    print("Manhattan path length: " + str(len(path_manhattan)))
                    print("Euclidean path: " + str(path_euclidean))
                    print("Euclidean path length: " + str(len(path_euclidean)))
                    print("Zero distance: " + str(path_zero))
                    print("Zero distance path length: " + str(len(path_zero)))
                    different_paths = [path_diagonal, path_manhattan, path_euclidean, path_zero]
                    best_path = min(different_paths, key=len)
                    for i in range(len(different_paths)):
                        if different_paths[i] == best_path:
                            show_algorithm_in_progress = True
                            if i == 0:
                                name_of_tool = "Diagonal distance"
                                a_star(starting_node, diagonal_distance)
                            elif i == 1:
                                name_of_tool = "Manhattan distance"
                                a_star(starting_node, manhattan_distance)
                            elif i == 2:
                                name_of_tool = "Euclidean distance"
                                a_star(starting_node, euclidean_distance)
                            elif i == 3:
                                bruteforce_dijkstra = True
                                name_of_tool = "Zero distance"
                                a_star(starting_node, zero_distance)
                            break
                    hit_enter = True
                    print("Best path: " + str(best_path))
                    print("Tool used: " + str(name_of_tool))
                    maze = np.swapaxes(maze,0,1)
                # If the maze is impossible to complete, this information gets printed to the console
                except TypeError as e:
                    print("There is no solution to this maze!")
                    #print(e)
                    pygame.quit()
                    sys.exit()
        if four_used_up == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for idx in range(len(input_box_list)):
                    if input_box_list[idx]["rectangle"].collidepoint(event.pos):
                        if three_used_up == False:
                            #print(idx)
                            #print(input_box_list[idx]["coordinates"])
                            # The first click will establish the maze's starting node.
                            # The maze can be changed because the list 'input_box_list' is a list of dictionaries,
                            # with each dictionary storing the location of a specific box in the game. These dictionaries
                            # also keep track of where the index values of that box would be if it instead existed in the maze list. 
                            maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] = 3
                            first_coord = input_box_list[idx]["coordinates"][0]
                            second_coord = input_box_list[idx]["coordinates"][1]
                            starting_node = [second_coord, first_coord]
                            three_used_up = True
                        elif four_used_up == False:
                            #print(idx)
                            #print(input_box_list[idx]["coordinates"])
                            # The second click will establish the maze's ending node
                            maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] = 4
                            first_coord = input_box_list[idx]["coordinates"][0]
                            second_coord = input_box_list[idx]["coordinates"][1]
                            ending_node = [second_coord, first_coord]
                            four_used_up = True
                        else:
                            #print(idx)
                            #print(input_box_list[idx]["coordinates"])
                            # Subsequent clicks create barriers in the path
                            print(maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]])
                            maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] = 1

        elif pygame.mouse.get_pressed()[0]:
            remove_fastest_path_after_clicking = True
            # Tracks whether the mouse button is held down
            # There will be an AttributeError if the user holds down the mouse and then goes offscreen. When this occurs, the error is ignored.
            try:
                for idx in range(len(input_box_list)):
                    if input_box_list[idx]["rectangle"].collidepoint(event.pos):
                        if maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] != 3 and maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] != 4:
                            maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] = 1
            except AttributeError:
                pass

                    
'''
printer(maze)
actual_maze = np.array(maze)
actual_maze = np.swapaxes(actual_maze,0,1)
printer(actual_maze)
print(starting_node)
print(ending_node)
'''