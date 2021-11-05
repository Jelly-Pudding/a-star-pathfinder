from pathfinder import *
import pygame

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
print(num_of_rows)
print(num_of_cols)

maze = [[0 for col in range(num_of_cols)] for row in range(num_of_rows)]

printer(maze)

pygame.init()
screen = pygame.display.set_mode((num_of_rows * 20, num_of_cols * 20))
print(pygame.display.get_window_size())
#each box will be 5x5

input_box_list = []
for i in range(len(maze)):
    for j in range(len(maze[i])):
        input_box_list.append({"rectangle": pygame.Rect(20*i, 20*j, 20, 20), "coordinates": [j, i]})

print(input_box_list)

input_box2 = pygame.Rect(30, 115, 150, 32)

def game_display():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[j][i] == 3:
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(20*i, 20*j, 20, 20))
            else:
                pygame.draw.rect(screen, (40,40,40), pygame.Rect(20*i, 20*j, 20, 20))
    """
    for index_of_item in range(len(input_box_list)):
        pygame.draw.rect(screen, (40,40,40), input_box_list[index_of_item]["rectangle"])
    """
    for i in range(len(maze)):
        pygame.draw.line(screen, (255, 255, 255), (i*20, 0), (i*20, num_of_cols*20), 2)
        for j in range(len(maze[i])):
            pygame.draw.line(screen, (255, 255, 255), (0, j*20), (num_of_rows*20, j*20), 2)

    #line across the bottom

    pygame.draw.line(screen, (255, 255, 255), (0, num_of_cols*20), (num_of_rows*20, num_of_cols*20), 4)

    #line down the right hand side

    pygame.draw.line(screen, (255, 255, 255), (num_of_rows*20, 0), (num_of_rows*20, num_of_cols*20), 4)

    pygame.display.update()

running = True

while running:
    game_display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for idx in range(len(input_box_list)):
                if input_box_list[idx]["rectangle"].collidepoint(event.pos):
                    print(idx)
                    print(input_box_list[idx]["coordinates"])
                    maze[input_box_list[idx]["coordinates"][0]][input_box_list[idx]["coordinates"][1]] = 3

printer(maze)

