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

def game_display():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            pygame.draw.rect(screen, (0, 255, 0), (20*i, 20*j, 20, 20))

    for i in range(len(maze)):
        pygame.draw.line(screen, (255, 255, 255), (i*20, 0), (i*20, num_of_cols*20), 2)
        for j in range(len(maze[i])):
            pygame.draw.line(screen, (255, 255, 255), (0, j*20), (num_of_rows*20, j*20), 2)

    #line across the bottom

    pygame.draw.line(screen, (255, 255, 255), (0, num_of_cols*20), (num_of_rows*20, num_of_cols*20), 4)

    #line down the right hand side

    pygame.draw.line(screen, (255, 255, 255), (num_of_rows*20, 0), (num_of_rows*20, num_of_cols*20), 4)

    '''
    pygame.draw.line(screen, (255, 255, 255), (20, 0), (20, 200), 2)
    pygame.draw.line(screen, (255, 255, 255), (40, 0), (40, 200), 2)
    pygame.draw.line(screen, (255, 255, 255), (60, 0), (60, 200), 2)
    pygame.draw.line(screen, (255, 255, 255), (80, 0), (80, 200), 2)
    pygame.draw.line(screen, (255, 255, 255), (100, 0), (100, 200), 2)
    pygame.draw.line(screen, (255, 255, 255), (120, 0), (120, 200), 2)
    pygame.draw.line(screen, (255, 255, 255), (140, 0), (140, 200), 2)
    pygame.draw.line(screen, (255, 255, 255), (160, 0), (160, 200), 2)
    pygame.draw.line(screen, (255, 255, 255), (180, 0), (180, 200), 2)


    pygame.draw.line(screen, (255, 255, 255), (0, 20), (200, 20), 2)
    pygame.draw.line(screen, (255, 255, 255), (0, 40), (200, 40), 2)
    pygame.draw.line(screen, (255, 255, 255), (0, 60), (200, 60), 2)
    pygame.draw.line(screen, (255, 255, 255), (0, 80), (200, 80), 2)
    pygame.draw.line(screen, (255, 255, 255), (0, 100), (200, 100), 2)
    pygame.draw.line(screen, (255, 255, 255), (0, 120), (200, 120), 2)
    pygame.draw.line(screen, (255, 255, 255), (0, 140), (200, 140), 2)
    pygame.draw.line(screen, (255, 255, 255), (0, 160), (200, 160), 2)
    pygame.draw.line(screen, (255, 255, 255), (0, 180), (200, 180), 2)
    '''
    '''
    pygame.draw.rect(screen, (0, 255, 0), (0, 0, 20, 20))
    pygame.draw.rect(screen, (0, 255, 0), (20, 0, 20, 20))
    pygame.draw.rect(screen, (0, 255, 0), (40, 0, 20, 20))
    pygame.draw.rect(screen, (0, 255, 0), (60, 0, 20, 20))
    pygame.draw.rect(screen, (0, 255, 0), (80, 0, 20, 20))
    pygame.draw.rect(screen, (0, 255, 0), (100, 0, 20, 20))
    pygame.draw.rect(screen, (0, 255, 0), (120, 0, 20, 20))
    pygame.draw.rect(screen, (0, 255, 0), (140, 0, 20, 20))
    pygame.draw.rect(screen, (0, 255, 0), (160, 0, 20, 20))
    pygame.draw.rect(screen, (0, 255, 0), (180, 0, 20, 20))
    '''
        

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

