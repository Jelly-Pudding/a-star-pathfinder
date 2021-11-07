import pygame
import numpy as np
import time
import sys


#default size of row and column
num_of_rows = 10
num_of_cols = 10
pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.font.init()
pygame.display.set_caption('Select Size')
myfont = pygame.font.SysFont("timesnewroman", 30)
text = myfont.render("start game", True, (255,255,255))
input_box1 = pygame.Rect(30, 45, 150, 32)
input_box2 = pygame.Rect(30, 115, 150, 32)
done_box = pygame.Rect(50, 160, 110, 25)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
active1 = False
active2 = False
input_text = ""
input_text2 = ""

def displayer():
    textsurface = myfont.render("Enter Row#:", False, (90, 0, 0))
    screen.blit(textsurface,(30,10))
    secondquestion = myfont.render("Enter Column#:", False, (90, 0, 0))
    screen.blit(secondquestion,(7,80))
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

num_of_rows = int(num_of_rows)
num_of_cols = int(num_of_cols)
#print(num_of_rows)
#print(num_of_cols)

maze = [[0 for col in range(num_of_cols)] for row in range(num_of_rows)]

#printer(maze)

pygame.init()

#each box (or node) will be 20x20. Therefore, width (number of rows) and height (number of columns) are multiplied by 20 so there is the exact amount of space needed for every box.

screen = pygame.display.set_mode((num_of_rows * 20, num_of_cols * 20))

#This list places the positioning of every box on the screen in a unique dictionary, and the dictionaries also store where
#the corresponding node will be in the maze list (referred to in the dictionary's key as "coordinates")

input_box_list = []
for i in range(len(maze)):
    for j in range(len(maze[i])):
        input_box_list.append({"rectangle": pygame.Rect(20*i, 20*j, 20, 20), "coordinates": [i, j]})


#if the enter key is pressed, then the a* algorithm starts and this variable becomes True

hit_enter = False

def game_display():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            #the starting node (shown as blue)
            if maze[i][j] == 3:
                pygame.draw.rect(screen, (0,0,255), pygame.Rect(20*i, 20*j, 20, 20))
            #the ending node (shown as green)
            elif maze[i][j] == 4:
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(20*i, 20*j, 20, 20))
            #barriers in the path (shown as red)
            elif maze[i][j] == 1:
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(20*i, 20*j, 20, 20)) 
            #normal nodes (shown as grey)        
            else:
                pygame.draw.rect(screen, (40,40,40), pygame.Rect(20*i, 20*j, 20, 20))

    if hit_enter == True:
        for items in best_path:
            pygame.draw.rect(screen, (0,255,0), pygame.Rect(20*items[1], 20*items[0], 20, 20))

    #lines to separate the boxes from one another

    for i in range(len(maze)):
        pygame.draw.line(screen, (255, 255, 255), (i*20, 0), (i*20, num_of_cols*20), 2)
        for j in range(len(maze[i])):
            pygame.draw.line(screen, (255, 255, 255), (0, j*20), (num_of_rows*20, j*20), 2)

    #line across the bottom

    pygame.draw.line(screen, (255, 255, 255), (0, num_of_cols*20), (num_of_rows*20, num_of_cols*20), 4)

    #line down the right hand side

    pygame.draw.line(screen, (255, 255, 255), (num_of_rows*20, 0), (num_of_rows*20, num_of_cols*20), 4)

    pygame.display.update()

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
    two_d = []
    two_d = list(map(list, zip(new_nodes_0, new_nodes_1)))
    # if the index is greater than the row or column, it is converted to a negative number (so it can be dealt with afterwards)
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

def manhattan_distance(node):
    h = abs(node[0] - ending_node[0]) + abs(node[1] - ending_node[1])
    return h

def diagonal_distance(node):
    dx = abs(node[0] - ending_node[0])
    dy = abs(node[1] - ending_node[1])
    #Assumes length of nodes is 1, and thus the diagonal distance between nodes is the square root of 2.
    #These numbers are multiplied by 10 to give 10 and 14.
    h = 10 * (dx + dy) + (14 - 2 * 10) * min(dx, dy)
    return h

def euclidean_distance(node):
    node_numpy = np.array(node)
    ending_node_numpy = np.array(ending_node)
    return np.linalg.norm(node_numpy - ending_node_numpy)



#When this is set to True, the a* function will show the algorithm trying out different paths to the end node.
show_algorithm_in_progress = False


def a_star(starting_node, distance_till_end_function):
    child_count = 0 
    count = 0
    path = []
    unseen_list = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            unseen_list.append({"the_node": [i, j]})
    #print(unseen_list)
    open_list = []
    closed_list = []
    open_list.append({"the_node": starting_node, "parent": None, "g_value": 0, "f_value": 0})
    #count = 0
    while open_list != []:
        #count += 1
        #print(count)
        #deals with the current node
        dict_with_lowest_f_value = min(open_list, key=lambda x:x["f_value"])
        current_node = dict_with_lowest_f_value["the_node"]
        parent_of_current_node = dict_with_lowest_f_value["parent"]
        current_node_g_value = dict_with_lowest_f_value["g_value"]  
        current_node_index = next((index for (index, d) in enumerate(open_list) if d["the_node"] == current_node), None)
        #print("open_list before pop: " + str(open_list))
        open_list.pop(current_node_index)

        #print("open_list after pop: " + str(open_list))

        children = find_adjacent_nodes(current_node)
        for child in children:
            parent = current_node
            closed_current_node_index = next((index for (index, d) in enumerate(closed_list) if d["the_node"] == current_node), None)
            child_dist_from_start = current_node_g_value + 1
            child_dist_from_end = distance_till_end_function(child)
            child_f = child_dist_from_start + child_dist_from_end

            if child == ending_node:
                #print("\n")
                #print("open " + str(open_list) + "\n")
                #print("closed " + str(closed_list))
                #print("parent of current node:" + str(parent_of_current_node))
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


            if show_algorithm_in_progress == True:
                time.sleep(0.1)
                pygame.draw.rect(screen, (255,192,203), pygame.Rect(20*child[1], 20*child[0], 20, 20))
                pygame.draw.rect(screen, (255,40,90), pygame.Rect(20*current_node[1], 20*current_node[0], 20, 20))
                for items in closed_list:
                    pygame.draw.rect(screen, (0,0,0), pygame.Rect(20*items["the_node"][1], 20*items["the_node"][0], 20, 20))    
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
                for items in current_fastest_path:
                    pygame.draw.rect(screen, (150,255,220), pygame.Rect(20*items[1], 20*items[0], 20, 20))
                for i in range(len(maze)):
                    pygame.draw.line(screen, (255, 255, 255), (i*20, 0), (i*20, num_of_cols*20), 2)
                    for j in range(len(maze[i])):
                        pygame.draw.line(screen, (255, 255, 255), (0, j*20), (num_of_rows*20, j*20), 2)
                pygame.display.update()

        closed_list.append(dict_with_lowest_f_value)

        #print("closed list at end of while loop: " + str(closed_list))
        #print("open list at end of while loop: " + str(open_list))

running = True

#3 represents the starting node, and #4 the ending node (or goal node). Each should only be placed once, so these bool variables keep track of whether they have been placed.

three_used_up = False
four_used_up = False



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
            elif event.key == pygame.K_RETURN:
                maze = np.array(maze)
                maze = np.swapaxes(maze,0,1)
                #print("adjacent nodes = " + str(find_adjacent_nodes([0, 3])))
                print(maze)
                path_manhattan = a_star(starting_node, manhattan_distance)
                path_diagonal = a_star(starting_node, diagonal_distance)
                path_euclidean = a_star(starting_node, euclidean_distance)
                print("manhattan path = " + str(path_manhattan))
                print("manhattan path length:" + str(len(path_manhattan)))
                print("diagonal path = " + str(path_diagonal))
                print("diagonal path length:" + str(len(path_diagonal)))
                print("euclidean path = " + str(path_euclidean))
                print("euclidean path length:" + str(len(path_euclidean)))
                different_paths = [path_manhattan, path_diagonal, path_euclidean]
                best_path = min(different_paths, key=len)
                for i in range(len(different_paths)):
                    if different_paths[i] == best_path:
                        show_algorithm_in_progress = True
                        if i == 0:
                            name_of_tool = "manhattan"
                            a_star(starting_node, manhattan_distance)
                        elif i == 1:
                            name_of_tool = "diagonal"
                            a_star(starting_node, diagonal_distance)
                        else:
                            name_of_tool = "euclidean"
                            a_star(starting_node, euclidean_distance)
                        break
                hit_enter = True
                print("best path - " + str(best_path))
                print("Tool used: " + str(name_of_tool))
                maze = np.swapaxes(maze,0,1)

        if pygame.mouse.get_pressed()[0]:
            for idx in range(len(input_box_list)):
                if input_box_list[idx]["rectangle"].collidepoint(event.pos):
                    if three_used_up == False:
                        #print(idx)
                        #print(input_box_list[idx]["coordinates"])
                        #The first click will establish the maze's starting node.
                        #The maze can be changed because the list 'input_box_list' is a list of dictionaries,
                        #with each dictionary storing the location of a specific box in the game. These dictionaries
                        #also keep track of where the index values of that box would be if it instead existed in the maze list. 
                        maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] = 3
                        first_coord = input_box_list[idx]["coordinates"][0]
                        second_coord = input_box_list[idx]["coordinates"][1]
                        starting_node = [second_coord, first_coord]
                        three_used_up = True
                    elif four_used_up == False:
                        #print(idx)
                        #print(input_box_list[idx]["coordinates"])
                        #The second click will establish the maze's ending node
                        maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] = 4
                        first_coord = input_box_list[idx]["coordinates"][0]
                        second_coord = input_box_list[idx]["coordinates"][1]
                        ending_node = [second_coord, first_coord]
                        four_used_up = True
                    else:
                        #print(idx)
                        #print(input_box_list[idx]["coordinates"])
                        #Subsequent clicks create barriers in the path
                        maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] = 1

                    
'''
printer(maze)

actual_maze = np.array(maze)
actual_maze = np.swapaxes(actual_maze,0,1)

printer(actual_maze)
print(starting_node)
print(ending_node)
'''