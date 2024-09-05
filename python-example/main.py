import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
OBJECT_WIDTH = 50
OBJECT_HEIGHT = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Pygame Game")

# Load sound effects
move_sound = pygame.mixer.Sound("move.wav")
collision_sound = pygame.mixer.Sound("collision.wav")

# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.speed = 5

    def move(self, dx):
        if 0 <= self.rect.x + dx <= SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x += dx
            move_sound.play()

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

# Falling object class
class FallingObject:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - OBJECT_WIDTH), 0, OBJECT_WIDTH, OBJECT_HEIGHT)
        self.speed = random.randint(3, 7)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

# Main game function
def main():
    clock = pygame.time.Clock()
    player = Player()
    objects = [FallingObject() for _ in range(5)]
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player.speed)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed)

        for obj in objects:
            obj.fall()
            if obj.rect.y > SCREEN_HEIGHT:
                obj.rect.y = 0
                obj.rect.x = random.randint(0, SCREEN_WIDTH - OBJECT_WIDTH)
            if player.rect.colliderect(obj.rect):
                collision_sound.play()
                running = False  # End game on collision

        player.draw(screen)
        for obj in objects:
            obj.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()