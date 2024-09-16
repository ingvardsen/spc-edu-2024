import pygame
import sys

# Initialiser pygame
pygame.init()

# Definer farver
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Skærmstørrelse
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

clock = pygame.time.Clock()

# Paddles
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Bold
BALL_SIZE = 15

# Paddle positioner
paddle1_pos = [10, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2]
paddle2_pos = [SCREEN_WIDTH - 10 - PADDLE_WIDTH, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2]

# Bold position og hastighed
ball_pos = [SCREEN_WIDTH//2, SCREEN_HEIGHT//2]
ball_vel = [4, 4]

# Kontroller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)

def draw():
    screen.fill(BLACK)
    # Tegn paddles
    pygame.draw.rect(screen, WHITE, (paddle1_pos[0], paddle1_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (paddle2_pos[0], paddle2_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    # Tegn bold
    pygame.draw.rect(screen, WHITE, (ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Bevægelser for paddle1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1_pos[1] -= 5
    if keys[pygame.K_s]:
        paddle1_pos[1] += 5
    if keys[pygame.K_UP]:
        paddle2_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        paddle2_pos[1] += 5

    # Game controller input
    for i, joystick in enumerate(joysticks):
        axis_y = joystick.get_axis(1)
        if i == 0:
            paddle1_pos[1] += int(axis_y * 5)
        elif i == 1:
            paddle2_pos[1] += int(axis_y * 5)

    # Begræns paddles til skærmen
    paddle1_pos[1] = max(min(paddle1_pos[1], SCREEN_HEIGHT - PADDLE_HEIGHT), 0)
    paddle2_pos[1] = max(min(paddle2_pos[1], SCREEN_HEIGHT - PADDLE_HEIGHT), 0)

    # Flyt bold
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Kollision med top og bund
    if ball_pos[1] <= 0 or ball_pos[1] >= SCREEN_HEIGHT - BALL_SIZE:
        ball_vel[1] = -ball_vel[1]

    # Kollision med paddles
    if (ball_pos[0] <= paddle1_pos[0] + PADDLE_WIDTH and
        paddle1_pos[1] < ball_pos[1] < paddle1_pos[1] + PADDLE_HEIGHT):
        ball_vel[0] = -ball_vel[0]
    if (ball_pos[0] >= paddle2_pos[0] - BALL_SIZE and
        paddle2_pos[1] < ball_pos[1] < paddle2_pos[1] + PADDLE_HEIGHT):
        ball_vel[0] = -ball_vel[0]

    # Reset bold hvis den går ud af skærmen
    if ball_pos[0] <= 0 or ball_pos[0] >= SCREEN_WIDTH - BALL_SIZE:
        ball_pos = [SCREEN_WIDTH//2, SCREEN_HEIGHT//2]
        ball_vel[0] = -ball_vel[0]

    draw()
    clock.tick(60)
