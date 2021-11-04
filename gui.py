from pathfinder import *
import pygame


print(maze[6][6])
print(row)
print(column)




screen = pygame.display.set_mode((200, 200))
pygame.font.init()
pygame.display.set_caption('A*')
myfont = pygame.font.SysFont("timesnewroman", 30)
text = myfont.render("start game", True, (255,255,255))
input_box1 = pygame.Rect(39, 70, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
active = False
input_text = ""

def displayer():
    textsurface = myfont.render('Enter Row:', False, (65, 0, 0))
    screen.blit(textsurface,(40,30))
    if active == True:
        pygame.draw.rect(screen, color_active, input_box1)
    else:
        pygame.draw.rect(screen, color_inactive, input_box1)
    second_text = myfont.render(input_text, True, (50, 0, 0))
    screen.blit(second_text, (39,70))
    pygame.display.update()

running = True
  
while running:  
    displayer()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box1.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if active == True:
                if event.key == pygame.K_RETURN:
                    num_of_rows = input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

print(num_of_rows)
