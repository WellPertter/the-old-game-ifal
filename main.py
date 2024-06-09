import pygame
import random

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo dos Quadrados")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)  # Rosa

# Tamanho dos quadrados
SQUARE_SIZE = 20

# Pontuação
score = 0

class Player:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.direction = 1

    def move(self, keys, left_key, right_key):
        if keys[left_key]:
            self.direction = -1
        elif keys[right_key]:
            self.direction = 1

    def update_position(self, width):
        self.x += self.direction * self.speed
        if self.x < 0:
            self.x = 0
            self.direction = 1
        elif self.x > width - self.size:
            self.x = width - self.size
            self.direction = -1

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size))

    def get_center(self):
        return self.x + self.size // 2

class Target:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def relocate(self, width):
        positions = [i * SQUARE_SIZE for i in range(width // SQUARE_SIZE)]
        self.x = random.choice(positions)
        self.y = 10

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size))

class Bullet:
    def __init__(self, size, speed):
        self.x = 0
        self.y = 0
        self.size = size
        self.speed = speed
        self.active = False

    def shoot(self, player_center_x, player_y):
        if not self.active:
            self.active = True
            self.x = player_center_x - self.size // 2
            self.y = player_y

    def move(self):
        if self.active:
            self.y -= self.speed
            if self.y < 0:
                self.active = False

    def draw(self, win, color):
        if self.active:
            pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size))

# Instanciar objetos
player = Player(WIDTH // 2 - SQUARE_SIZE // 2, HEIGHT - SQUARE_SIZE - 10, SQUARE_SIZE, SQUARE_SIZE)
target = Target(random.randint(0, WIDTH // SQUARE_SIZE - 1) * SQUARE_SIZE, 10, SQUARE_SIZE)
bullet = Bullet(SQUARE_SIZE, 10)

# Fonte para a pontuação
font = pygame.font.SysFont(None, 36)

# Loop principal do jogo
running = True
while running:
    pygame.time.delay(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    player.move(keys, pygame.K_LEFT, pygame.K_RIGHT)

    # Atualizar posição do jogador
    player.update_position(WIDTH)

    # Disparo do projétil do jogador
    if keys[pygame.K_SPACE]:
        bullet.shoot(player.get_center(), player.y)

    # Atualizar posição do projétil
    bullet.move()

    # Colisão entre projétil do jogador e o alvo
    if (bullet.active and
        bullet.x in range(target.x, target.x + target.size) and 
        bullet.y in range(target.y, target.y + target.size)):
        score += 1
        target.relocate(WIDTH)
        bullet.active = False

    # Desenhar tudo na tela
    win.fill(WHITE)
    target.draw(win, RED)

    # Desenhar o indicador de tiro (quadrado rosa) na mesma linha do jogador, espelhado na posição do alvo
    pink_x = target.x
    pink_y = player.y
    
    pygame.draw.rect(win, PINK, (pink_x, pink_y, SQUARE_SIZE, SQUARE_SIZE))
    player.draw(win, BLUE)
    bullet.draw(win, GREEN)

    # Desenhar pontuação em amarelo
    score_text = font.render(f"Score: {score}", True, YELLOW)
    win.blit(score_text, (10, 10))
    
    pygame.display.update()

pygame.quit()
