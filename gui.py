from pathfinder import *
import pygame

#default size of row and column
num_of_rows = 10
num_of_cols = 10

screen = pygame.display.set_mode((200, 200))
pygame.font.init()
pygame.display.set_caption('A*')
myfont = pygame.font.SysFont("timesnewroman", 30)
text = myfont.render("start game", True, (255,255,255))
input_box1 = pygame.Rect(30, 45, 150, 32)
input_box2 = pygame.Rect(30, 115, 150, 32)
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
    pygame.display.update()

running = True
  
while running:  
    displayer()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if active1 == True:
                if event.key == pygame.K_RETURN:
                    num_of_rows = input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    num_of_rows = input_text
                else:
                    input_text += event.unicode
                    num_of_rows = input_text
            if active2 == True:
                if event.key == pygame.K_RETURN:
                    num_of_cols = input_text2
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text2[:-1]
                    num_of_rows = input_text2
                else:
                    input_text2 += event.unicode
                    num_of_rows = input_text2

print(num_of_rows)
print(num_of_cols)
