import pygame
import random
import time
import math

# Initialize game window
pygame.init()

# Snake coordinates
snakeX = 245
snakeY = 245
snakeX_list = []
snakeY_list = []
snakeX_list.append(snakeX)
snakeY_list.append(snakeY)

snakeX_change = 0
snakeY_change = 0

# Food
food_status = "eaten"
foodX = random.randint(0, 490)
foodY = random.randint(0, 490)

# Score
score = 0
score_font = pygame.font.SysFont('freesansbold.tff', 32)

# Game over
over_font = pygame.font.SysFont('freesansbold.tff', 40)


def boundary_collision_check(snakeHead = 0):
    global game_running, snakeX_list, snakeY_list, snakeX_change, snakeY_change
    # Boundary collision check
    if snakeX_list[snakeHead] >= 490 or snakeX_list[snakeHead] < 0 or snakeY_list[snakeHead] >= 490 or snakeY_list[
        snakeHead] < 0:
        snakeX_list[snakeHead] = snakeX_list[snakeHead]
        snakeY_list[snakeHead] = snakeY_list[snakeHead]
        snakeX_change = 0
        snakeY_change = 0
        game_running = False


# Body collision check
def body_collision_check(snakeHead=0):
    global game_running, snakeX_list, snakeY_list, snakeX_change, snakeY_change
    for i in range(2, len(snakeY_list)):
        if isCollsion(snakeX_list[snakeHead], snakeY_list[snakeHead], snakeX_list[i], snakeY_list[i]):
            game_running = False


# Calculate collision
def isCollsion(x_1, y_1, x_2, y_2):
    distance = math.sqrt(((x_1 - x_2) ** 2) + ((y_1 - y_2) ** 2))
    if 0 <= distance < 10:
        return True
    else:
        return False


def game_over():
    screen.fill((0, 0, 0))
    over_text = over_font.render("GAME OVER: YOU LOSE", True, (255, 255, 255))
    screen.blit(over_text, (80, 250))


# First food generation:
def food_draw(food_status):
    global screen, foodX, foodY
    if food_status == "eaten":
        pygame.draw.rect(screen, (255, 255, 255), (foodX, foodY, 10, 10))


def show_score():
    global score
    score_show = score_font.render("Score: " + str(score) + " ", True, (255, 255, 255))
    screen.blit(score_show, (10, 10))


# Generate multiple food
def food_generation(food_status, snakeHead=0):
    global snakeX_list, snakeY_list, foodX, foodY, score
    food_draw(food_status)

    for i in range(1, len(snakeX_list)):
        if isCollsion(snakeX_list[snakeHead], snakeY_list[snakeHead], foodX, foodY):
            food_status = "eaten"
            pygame.draw.rect(screen, (0, 0, 0), (foodX, foodY, 10, 10))
            score = len(snakeX_list) - 1
            foodX = random.randint(0, 490)
            foodY = random.randint(0, 490)
            food_generation(food_status, snakeHead)

        elif isCollsion(snakeX_list[i], snakeY_list[i], foodX, foodY):
            food_generation(food_status, snakeHead)


# Movement with body
def snake_move():
    global snakeX_list, snakeY_list, snakeX_change, snakeY_change
    new_X_list = snakeX_list[0:-1]
    new_Y_list = snakeY_list[0:-1]

    for j in range(0, len(new_X_list)):
        if snakeX_change == 0 and snakeY_change == 0:
            break
        else:
            del snakeX_list[1:]
            del snakeY_list[1:]
            snakeX_list += new_X_list
            snakeY_list += new_Y_list

    snakeX_list[0] += snakeX_change
    snakeY_list[0] += snakeY_change


def add_body():
    global snakeX_list, snakeY_list, foodY, foodX

    if len(snakeX_list) > 1:
        if isCollsion(snakeX_list[0], snakeY_list[0], foodX, foodY):
            if snakeX_list[-1] - snakeX_list[-2] == -10 and snakeY_list[-1] - snakeY_list[-2] == 0:  # To the left
                snakeX_list.append(snakeX_list[-1] - 10)
                snakeY_list.append(snakeY_list[-1])
            elif snakeX_list[-1] - snakeX_list[-2] == 10 and snakeY_list[-1] - snakeY_list[-2] == 0:  # To the right
                snakeX_list.append(snakeX_list[-1] + 10)
                snakeY_list.append(snakeY_list[-1])
            elif snakeX_list[-1] - snakeX_list[-2] == 0 and snakeY_list[-1] - snakeY_list[-2] == 10:  # Upwards
                snakeX_list.append(snakeX_list[-1])
                snakeY_list.append(snakeY_list[-1] + 10)
            elif snakeX_list[-1] - snakeX_list[-2] == 0 and snakeY_list[-1] - snakeY_list[-2] == -10:  # Downwards
                snakeX_list.append(snakeX_list[-1])
                snakeY_list.append(snakeY_list[-1] - 10)

    elif len(snakeX_list) == 1:
        if isCollsion(snakeX_list[0], snakeY_list[0], foodX, foodY):
            if snakeX_change == 10 and snakeY_change == 0:  # Right
                snakeX_list.append(snakeX_list[0] - 10)
                snakeY_list.append(snakeY_list[0])
            elif snakeX_change == -10 and snakeY_change == 0:  # Left
                snakeX_list.append(snakeX_list[0] + 10)
                snakeY_list.append(snakeY_list[0])
            elif snakeX_change == 0 and snakeY_change == 10:  # Down
                snakeX_list.append(snakeX_list[0])
                snakeY_list.append(snakeY_list[0] - 10)
            elif snakeX_change == 0 and snakeY_change == -10:  # Up
                snakeX_list.append(snakeX_list[0])
                snakeY_list.append(snakeY_list[0] + 10)


def keyboard():
    global snakeX_change, snakeY_change, snakeX_list, game_running
    for event in pygame.event.get():
        # Movement
        if event.type == pygame.KEYDOWN:
            if len(snakeX_list) == 1:
                if event.key == pygame.K_LEFT:
                    snakeY_change = 0
                    snakeX_change = -10

                elif event.key == pygame.K_RIGHT:
                    snakeY_change = 0
                    snakeX_change = 10

                elif event.key == pygame.K_UP:
                    snakeY_change = -10
                    snakeX_change = 0

                elif event.key == pygame.K_DOWN:
                    snakeY_change = 10
                    snakeX_change = 0

            else:
                if event.key == pygame.K_LEFT:
                    if snakeY_change == 10 or snakeY_change == -10:
                        snakeY_change = 0
                        snakeX_change = -10
                    elif snakeX_change == 10:
                        snakeX_change = 10
                        snakeY_change = 0

                elif event.key == pygame.K_RIGHT:
                    if snakeY_change == 10 or snakeY_change == -10:
                        snakeY_change = 0
                        snakeX_change = 10
                    elif snakeX_change == -10:
                        snakeX_change = -10
                        snakeY_change = 0

                elif event.key == pygame.K_UP:
                    if snakeX_change == 10 or snakeX_change == -10:
                        snakeY_change = -10
                        snakeX_change = 0
                    elif snakeY_change == 10:
                        snakeY_change = 10
                        snakeX_change = 0

                elif event.key == pygame.K_DOWN:
                    if snakeX_change == 10 or snakeX_change == -10:
                        snakeY_change = 10
                        snakeX_change = 0
                    elif snakeY_change == -10:
                        snakeY_change = -10
                        snakeX_change = 0

        # Quitting the game
        if event.type == pygame.QUIT:
            game_running = False

# Game window icon and title
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Snake Game')
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)

# Running the game
game_running = True

# Frame and time settings
clock = pygame.time.Clock()


# Main code function
def main_game_system():
    global game_running, snakeX_change, snakeY_change, screen
    while game_running:
        keyboard()

        # Snake movement
        snake_move()

        # Adding tails
        add_body()

        # Draw snake
        screen.fill((0, 0, 0))
        for i in range(len(snakeX_list)):
            pygame.draw.rect(screen, (0, 255, 0), (snakeX_list[i], snakeY_list[i], 10, 10))

        # Boundary collision check
        boundary_collision_check(0)

        # Body collision check
        body_collision_check(0)

        # Generate food
        food_generation(food_status, 0)

        # Show score
        show_score()

        # Time frame
        clock.tick(20)

        if game_running == False:
            game_over()

        pygame.display.update()

        if game_running == False:
            pygame.time.delay(3500)


main_game_system()
