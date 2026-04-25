import pygame
import random
import os
import math

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (191, 105, 245)

SPEED = 5
COIN_WEIGHTS = [1, 2, 3]  # Different weights for coins
ENEMY_SPEED_INCREMENT = 20  # Increase in enemy speed after N coins collected
COINS_FOR_SPEED_INCREASE = 5  # Number of coins needed to increase enemy speed
ENEMY_INITIAL_SPEED = SPEED

FPS = 60


class Entity:
    def __init__(self, width, aspect_ratio, image_path, speed):
        self.width = width
        self.aspect_ratio = aspect_ratio
        self.height = self.width / self.aspect_ratio

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.MOVEMENT_SPEED = speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Obstacle(Entity):
    def __init__(self, width, aspect_ratio, image_path, speed):
        super().__init__(width, aspect_ratio, image_path, speed)
        self.rect.center = self.randomize_position()

    def randomize_position(self):
        y = int(-self.height)
        x = random.randint(10, SCREEN_WIDTH - 10 - self.rect.width)
        return x, y

    def move(self):
        self.rect.move_ip(0, self.MOVEMENT_SPEED)
        if self.rect.top > 600:
            self.__init__()


class Player(Entity):
    def __init__(self):
        super().__init__(60, 0.5, "images/car_purple.png", SPEED * 2)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.move_ip(-self.MOVEMENT_SPEED, 0)
        if pressed[pygame.K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH:
                self.rect.move_ip(self.MOVEMENT_SPEED, 0)


class Enemy(Obstacle):
    def __init__(self):
        colors_path = "images/cars"
        colors = os.listdir(colors_path)
        super().__init__(60, 0.5, colors_path + "/" + random.choice(colors), SPEED)
        self.image = pygame.transform.rotate(self.image, 180)

    def changeSpeed(self, speed):
        self.speed = speed


class Coin(Obstacle):
    def __init__(self):
        super().__init__(20, 1, "images/coin.png", SPEED)
        self.weight = random.choice(COIN_WEIGHTS)  # Assigning random weight to coin


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.font = pygame.font.SysFont("Courier New", 40)

        self.createBg()
        self.createEntities()
        self.createCounters()

    def createBg(self):
        self.bg = pygame.image.load("images/bg.png")
        bg_aspect_ratio = self.bg.get_width() / self.bg.get_height()
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, math.ceil(SCREEN_WIDTH / bg_aspect_ratio)))
        self.copies = math.ceil(SCREEN_HEIGHT / self.bg.get_height()) + 1

    def drawBg(self):
        self.screen.fill(WHITE)
        self.scroll = (self.scroll + self.speed // 1.5) % self.bg.get_height()
        for i in range(self.copies):
            self.screen.blit(self.bg, (0, self.scroll + (i - 1) * (self.bg.get_height() - 1)))

    def createCounters(self):
        self.scroll = 0
        self.coins = 0
        self.speed = SPEED
        self.enemies_speed_increment_count = 0  # Counter for counting coins to increase enemy speed

    def drawCoinCounter(self):
        pygame.draw.rect(self.screen, PURPLE, (SCREEN_WIDTH - 70, 0, 70, 60), border_radius=15)
        pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH - 65, 5, 60, 50), border_radius=10)
        coins_counter = self.font.render(str(self.coins), True, BLACK)
        text_rect = coins_counter.get_rect(center=(SCREEN_WIDTH - 35, 30))
        self.screen.blit(coins_counter, text_rect)

    def createEntities(self):
        self.player = Player()
        self.enemy = Enemy()
        self.coin = Coin()

    def drawEntities(self):
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        self.coin.draw(self.screen)
        self.player.move()
        self.enemy.move()
        self.coin.move()

    def watchCollisions(self):
        if self.player.rect.colliderect(self.enemy.rect):
            self.screen.fill(RED)
            self.running = False

        if self.player.rect.colliderect(self.coin.rect):
            self.coin.__init__()
            self.coins += self.coin.weight  # Increase coins by coin's weight
            self.enemies_speed_increment_count += self.coin.weight  # Increment counter for enemy speed increase
            if self.enemies_speed_increment_count >= COINS_FOR_SPEED_INCREASE:
                self.enemy.MOVEMENT_SPEED += ENEMY_SPEED_INCREMENT
                self.enemies_speed_increment_count = 0  # Reset the counter after increasing enemy speed

        if self.enemy.rect.colliderect(self.coin.rect):
            self.coin.__init__()

    def watchEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def drawGameOverScreen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))  
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("You lose", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.watchEvents()
            self.watchCollisions()
            self.drawBg()
            self.drawEntities()
            self.drawCoinCounter()
            pygame.display.flip()
            clock.tick(FPS)

        self.drawGameOverScreen()
        pygame.display.flip()

        pygame.time.wait(2000)


if __name__ == "__main__":
    game = Game()
    game.run()
