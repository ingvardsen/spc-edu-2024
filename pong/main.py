import pygame
import sys
import random
import time

# Initialiser pygame
pygame.init()

# Definer farver
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
CONFETTI_COLORS = [
    (255, 0, 0),   # Rød
    (0, 255, 0),   # Grøn
    (0, 0, 255),   # Blå
    (255, 255, 0), # Gul
    (255, 0, 255), # Magenta
    (0, 255, 255)  # Cyan
]
POWER_UP_COLORS = {
    'grow': (255, 215, 0),       # Guld
    'shrink': (139, 0, 139),     # Mørk magenta
    'speed': (0, 255, 127),      # Havgrøn
    'slow': (255, 69, 0),        # Orange rød
    'multi_ball': (65, 105, 225) # Kongeblå
}

# Opret fuldskærmsvindue
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Pong')

# Opdater skærmstørrelse
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

clock = pygame.time.Clock()

# Paddles
PADDLE_WIDTH = 10
PADDLE_HEIGHT = SCREEN_HEIGHT // 6  # Dynamisk baseret på skærmhøjde
PADDLE_SPEED = 5

# Bold
BALL_SIZE = 15

# Paddle positioner
paddle1_pos = [10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]
paddle2_pos = [SCREEN_WIDTH - 10 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2]

# Bold position og hastighed
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_vel = [4, 4]
balls = [{'pos': ball_pos.copy(), 'vel': ball_vel.copy()}]  # Liste over bolde

# Score
score1 = 0
score2 = 0

# Fonts
font = pygame.font.SysFont('Arial', 30)
big_font = pygame.font.SysFont('Arial', 60)

# Kontroller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)

# Konfetti data
confetti_particles = []
confetti_timer = 0
WINNING_SCORE = 10
game_over = False
winner = None

# Power-up data
power_ups = []
POWER_UP_SIZE = 20
POWER_UP_DURATION = 5  # sekunder

# Spillerens power-up status
paddle_power_up = {1: None, 2: None}
paddle_original_height = PADDLE_HEIGHT
paddle_original_speed = PADDLE_SPEED

def create_confetti():
    for _ in range(200):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(-SCREEN_HEIGHT, 0)
        speed = random.uniform(2, 7)
        color = random.choice(CONFETTI_COLORS)
        size = random.randint(5, 10)
        confetti_particles.append({'x': x, 'y': y, 'speed': speed, 'color': color, 'size': size})

def draw_confetti():
    for particle in confetti_particles:
        pygame.draw.rect(screen, particle['color'], (particle['x'], particle['y'], particle['size'], particle['size']))

def update_confetti():
    for particle in confetti_particles:
        particle['y'] += particle['speed']
        if particle['y'] > SCREEN_HEIGHT:
            particle['y'] = random.randint(-SCREEN_HEIGHT, 0)
            particle['x'] = random.randint(0, SCREEN_WIDTH)

def spawn_power_up():
    x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)
    y = random.randint(50, SCREEN_HEIGHT - 50)
    power_up_type = random.choice(['grow', 'shrink', 'speed', 'slow', 'multi_ball'])
    power_ups.append({'x': x, 'y': y, 'type': power_up_type, 'active': True})

def draw_power_ups():
    for pu in power_ups:
        if pu['active']:
            color = POWER_UP_COLORS[pu['type']]
            pygame.draw.rect(screen, color, (pu['x'], pu['y'], POWER_UP_SIZE, POWER_UP_SIZE), border_radius=5)

def check_power_up_collision():
    for pu in power_ups:
        if pu['active']:
            # Check collision with ball
            for ball in balls:
                ball_rect = pygame.Rect(ball['pos'][0], ball['pos'][1], BALL_SIZE, BALL_SIZE)
                pu_rect = pygame.Rect(pu['x'], pu['y'], POWER_UP_SIZE, POWER_UP_SIZE)
                if ball_rect.colliderect(pu_rect):
                    pu['active'] = False
                    if ball['vel'][0] > 0:
                        player = 2
                    else:
                        player = 1
                    paddle_power_up[player] = {'type': pu['type'], 'end_time': time.time() + POWER_UP_DURATION}
                    apply_power_up(player, pu['type'])
                    break

def apply_power_up(player, power_type):
    global PADDLE_HEIGHT, PADDLE_SPEED, balls
    if power_type == 'grow':
        PADDLE_HEIGHT *= 1.5
    elif power_type == 'shrink':
        PADDLE_HEIGHT *= 0.75
    elif power_type == 'speed':
        PADDLE_SPEED *= 1.5
    elif power_type == 'slow':
        PADDLE_SPEED *= 0.75
    elif power_type == 'multi_ball':
        new_ball = {'pos': balls[0]['pos'].copy(), 'vel': [-balls[0]['vel'][0], -balls[0]['vel'][1]]}
        balls.append(new_ball)

def remove_power_up(player):
    global PADDLE_HEIGHT, PADDLE_SPEED, paddle_original_height, paddle_original_speed
    if paddle_power_up[player] and time.time() > paddle_power_up[player]['end_time']:
        power_type = paddle_power_up[player]['type']
        if power_type == 'grow' or power_type == 'shrink':
            PADDLE_HEIGHT = paddle_original_height
        elif power_type == 'speed' or power_type == 'slow':
            PADDLE_SPEED = paddle_original_speed
        paddle_power_up[player] = None

def draw():
    # Tegn baggrund
    screen.fill(GRAY)
    
    # Tegn midterlinje
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)
    
    # Tegn paddles med afrundede hjørner
    pygame.draw.rect(screen, WHITE, (paddle1_pos[0], paddle1_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT), border_radius=10)
    pygame.draw.rect(screen, WHITE, (paddle2_pos[0], paddle2_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT), border_radius=10)
    
    # Tegn bolde som cirkler
    for ball in balls:
        pygame.draw.ellipse(screen, WHITE, (ball['pos'][0], ball['pos'][1], BALL_SIZE, BALL_SIZE))
    
    # Tegn score
    score_text = font.render(f'{score1}     {score2}', True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))
    
    # Tegn power-ups
    draw_power_ups()
    
    # Hvis spillet er slut, vis vinder og konfetti
    if game_over:
        win_text = big_font.render(f'{winner} vinder!', True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
        draw_confetti()
    
    pygame.display.flip()

# Hovedløkken
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Tillad afslutning af fuldskærm med ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if not game_over:
        # Bevægelser for paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1_pos[1] -= PADDLE_SPEED
        if keys[pygame.K_s]:
            paddle1_pos[1] += PADDLE_SPEED
        if keys[pygame.K_UP]:
            paddle2_pos[1] -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            paddle2_pos[1] += PADDLE_SPEED

        # Game controller input
        for i, joystick in enumerate(joysticks):
            axis_y = joystick.get_axis(1)
            if i == 0:
                paddle1_pos[1] += int(axis_y * PADDLE_SPEED)
            elif i == 1:
                paddle2_pos[1] += int(axis_y * PADDLE_SPEED)

        # Begræns paddles til skærmen
        paddle1_pos[1] = max(min(paddle1_pos[1], SCREEN_HEIGHT - PADDLE_HEIGHT), 0)
        paddle2_pos[1] = max(min(paddle2_pos[1], SCREEN_HEIGHT - PADDLE_HEIGHT), 0)

        # Flyt bolde
        for ball in balls:
            ball['pos'][0] += ball['vel'][0]
            ball['pos'][1] += ball['vel'][1]

            # Kollision med top og bund
            if ball['pos'][1] <= 0 or ball['pos'][1] >= SCREEN_HEIGHT - BALL_SIZE:
                ball['vel'][1] = -ball['vel'][1]

            # Kollision med paddles
            if (ball['pos'][0] <= paddle1_pos[0] + PADDLE_WIDTH and
                paddle1_pos[1] < ball['pos'][1] + BALL_SIZE and
                ball['pos'][1] < paddle1_pos[1] + PADDLE_HEIGHT):
                ball['vel'][0] = -ball['vel'][0]
            if (ball['pos'][0] + BALL_SIZE >= paddle2_pos[0] and
                paddle2_pos[1] < ball['pos'][1] + BALL_SIZE and
                ball['pos'][1] < paddle2_pos[1] + PADDLE_HEIGHT):
                ball['vel'][0] = -ball['vel'][0]

            # Score opdatering
            if ball['pos'][0] <= 0:
                score2 += 1
                balls.remove(ball)
                break
            if ball['pos'][0] >= SCREEN_WIDTH - BALL_SIZE:
                score1 += 1
                balls.remove(ball)
                break

        # Hvis alle bolde er væk, reset bold
        if len(balls) == 0:
            ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
            ball_vel = [4 * random.choice([-1, 1]), 4 * random.choice([-1, 1])]
            balls.append({'pos': ball_pos.copy(), 'vel': ball_vel.copy()})

        # Tjek for vinder
        if score1 >= WINNING_SCORE:
            game_over = True
            winner = "Spiller 1"
            create_confetti()
        elif score2 >= WINNING_SCORE:
            game_over = True
            winner = "Spiller 2"
            create_confetti()

        # Spawning power-ups
        if random.randint(1, 500) == 1:
            spawn_power_up()

        check_power_up_collision()

        # Fjern power-ups efter varighed
        remove_power_up(1)
        remove_power_up(2)
    else:
        # Opdater konfetti animation
        update_confetti()
        confetti_timer += 1
        if confetti_timer > 300:  # Vis konfetti i 5 sekunder (300 frames ved 60 fps)
            pygame.quit()
            sys.exit()

    draw()
    clock.tick(60)
