import pygame
from pygame.locals import *
import random
from tkinter import *

root = Tk()
root.title('Snake Game - Tutorial')
root.geometry('500x500')


def tab1():
    def tab2():
        label1.destroy()
        button1.destroy()
        label2 = Label(root, text='This is your classic game of Snake Game. This is the tutorial on how to play this game. '
                                  'The goal is to get the highest amount of red squares.'
                                  'to move you need to use the UP, DOWN, LEFT, RIGHT arrow keys to move around.'
                                  'the twist is that it moves very quickly so be ready!!!!!', font=('Times_New_Roman', 10))
        label2.place(relx=0.5, rely=0.5, anchor='center')  # Place text in the middle of the screen
        def back():
            label2.destroy()
            button2.destroy()
            tab1()
        button2 = Button(root, text='HOW TO PLAY', font=('Times_New_Roman', 10), command=back, activebackground='blue')
        button2.pack(side=BOTTOM)
    label1 = Label(root, text='TUTORIAL SCREEN', font=('Times_New_Roman', 15))
    label1.pack()

    button1 = Button(root, text='HOW TO PLAY', font=('Times_New_Roman', 10), command=tab2, activebackground='red')
    button1.pack(side=BOTTOM)


tab1()

root.mainloop()


pygame.init()

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

# define font
font = pygame.font.SysFont(None, 40)

# set up a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

# define snake variables
snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
snake_pos.append([300, 310])
snake_pos.append([300, 320])
snake_pos.append([300, 330])
direction = 1  # 1 is up, 2 is right, 3 is down, 4 is left

# define game variables
cell_size = 10
update_snake = 0
food = [0, 0]
new_food = True
new_piece = [0, 0]
game_over = False
clicked = False
score = 0

# define colors
bg = (115, 100, 125)
body_inner = (50, 175, 25)
body_outer = (100, 100, 200)
food_col = (200, 50, 50)
blue = (111, 13, 255)
red = (155, 0, 155)


def draw_screen():
    screen.fill(bg)


def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue)
    screen.blit(score_img, (0, 0))


def check_game_over(game_over):
    # first check is to see if the snake has eaten itself by checking if the head has clashed with the rest of the body
    head_count = 0
    for x in snake_pos:
        if snake_pos[0] == x and head_count > 0:
            game_over = True
        head_count += 1

    # second check is to see if the snake has gone out of bounds
    if snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] > screen_height:
        game_over = True

    return game_over


def draw_game_over():
    over_text = "Game Over!"
    over_img = font.render(over_text, True, blue)
    pygame.draw.rect(screen, red, (screen_width // 2 - 80, screen_height // 2 - 60, 160, 50))
    screen.blit(over_img, (screen_width // 2 - 80, screen_height // 2 - 50))

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))


run = True
while run:

    draw_screen()
    draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction = 4

    # create food
    if new_food:
        new_food = False
        food[0] = cell_size * random.randint(0, (screen_width // cell_size) - 1)
        food[1] = cell_size * random.randint(0, (screen_height // cell_size) - 1)

    # draw food
    pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))

    # check if food has been eaten
    if snake_pos[0] == food:
        new_food = True
        # create a new piece at the last point of the snake's tail
        new_piece = list(snake_pos[-1])
        # add an extra piece to the snake
        if direction == 1:
            new_piece[1] += cell_size
        # heading down
        if direction == 3:
            new_piece[1] -= cell_size
        # heading right
        if direction == 2:
            new_piece[0] -= cell_size
        # heading left
        if direction == 4:
            new_piece[0] += cell_size

        # attach new piece to the end of the snake
        snake_pos.append(new_piece)

        # increase score
        score += 1

    if not game_over:
        # update snake
        if update_snake > 99:
            update_snake = 0
            # first shift the positions of each snake piece back.
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            # now update the position of the head based on direction
            # heading up
            if direction == 1:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] - cell_size
            # heading down
            if direction == 3:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] + cell_size
            # heading right
            if direction == 2:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] + cell_size
            # heading left
            if direction == 4:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] - cell_size
            game_over = check_game_over(game_over)

    if game_over == True:
        draw_game_over()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            # reset variables
            game_over = False
            update_snake = 0
            food = [0, 0]
            new_food = True
            new_piece = [0, 0]
            # define snake variables
            snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
            snake_pos.append([300, 310])
            snake_pos.append([300, 320])
            snake_pos.append([300, 330])
            direction = 1  # 1 is up, 2 is right, 3 is down, 4 is left
            score = 0

    head = 1
    for x in snake_pos:

        if head == 0:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, (255, 0, 0), (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
            head = 0

    pygame.display.update()

    update_snake += 3

pygame.quit()