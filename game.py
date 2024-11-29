import pygame
import random
import csv

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("xomaldi.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Oboba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("oboba.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(-100, -50)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -50)
            self.rect.x = random.randint(0, SCREEN_WIDTH - 50)

class Tyvia(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("tyvia.png")
        self.image = pygame.transform.scale(self.image, (5, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.oboba_sprites = pygame.sprite.Group()
        self.tyvia_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.score = 0
        self.game_over = False

        for i in range(5):
            oboba = Oboba()
            self.all_sprites.add(oboba)
            self.oboba_sprites.add(oboba)

        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self):
        if not self.game_over:
            self.all_sprites.update()

            for tyvia in self.tyvia_sprites:
                enemies_hit = pygame.sprite.spritecollide(tyvia, self.oboba_sprites, True)
                for oboba in enemies_hit:
                    self.score += 1
                    tyvia.kill()
                    oboba = Oboba()
                    self.all_sprites.add(oboba)
                    self.oboba_sprites.add(oboba)

            if pygame.sprite.spritecollide(self.player, self.oboba_sprites, False):
                self.game_over = True

    def draw(self):
        screen.blit(self.background, (0, 0))

        self.all_sprites.draw(screen)

        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    def save_score(self):
        with open("high_scores.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.score])

    def show_high_scores(self):
        try:
            with open("high_scores.csv", "r") as file:
                reader = csv.reader(file)
                high_scores = [int(row[0]) for row in reader]
                high_scores.sort(reverse=True)
                high_scores = high_scores[:5]

            font = pygame.font.SysFont("Arial", 30)
            high_scores_text = font.render("High Scores:", True, WHITE)
            screen.blit(high_scores_text, (SCREEN_WIDTH // 2 - 100, 80))

            for i, score in enumerate(high_scores):
                score_text = font.render(f"{i+1}. {score}", True, WHITE)
                screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, 120 + i * 30))
        except FileNotFoundError:
            pass

def tamashi_spacewar():
    game = Game()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game = Game()
                if event.key == pygame.K_SPACE and not game.game_over:
                    tyvia = Tyvia(game.player.rect.centerx, game.player.rect.top)
                    game.all_sprites.add(tyvia)
                    game.tyvia_sprites.add(tyvia)

        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

        if game.game_over:
            game.save_score()

tamashi_spacewar()
