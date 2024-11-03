"""This project is an "Aim Trainer" application designed to help users improve
 their mouse accuracy and reaction time by clicking on randomly appearing targets. 
 Users aim to hit as many targets as possible within a given time, enhancing their 
 precision and speed."""

import math
import random
import time
import pygame

pygame.init()

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Aim Trainer")

# Time in milliseconds between new targets
TARGET_INCREMENT = 1000
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
LIVES = 3
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

import os

# Load the background image and handle errors if the file is not found
try:
    BG_IMAGE = pygame.image.load(os.path.join(os.getcwd(), "background.jpg"))
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, WIN.get_size())
except (pygame.error, FileNotFoundError):
    print("Unable to load background image.")
    BG_IMAGE = None
    # Fallback color


class Target:
    SIZE = 15
    COLOR = "yellow"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = self.SIZE
        self.creation_time = time.time()

    def draw(self, win):
        pygame.draw.circle(win, pygame.Color(self.COLOR), (self.x, self.y), self.size)

    def collide(self, x, y):
        dis = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return dis <= self.size

    def is_expired(self):
        return time.time() - self.creation_time > 1.75


def draw(win, targets):
    if BG_IMAGE:
        win.blit(BG_IMAGE, (0, 0))
    else:
        win.fill((0, 25, 40))

    for target in targets:
        target.draw(win)


def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"


def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, (169, 169, 169), (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))


def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill((0, 25, 40))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")

    accuracy = round(targets_pressed / clicks * 100, 1) if clicks > 0 else 0
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2


def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT and len(targets) == 0:
                x = random.randint(
                    TARGET_PADDING,
                    min(WIDTH - TARGET_PADDING, WIN.get_width() - TARGET_PADDING),
                )
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT,
                    min(HEIGHT - TARGET_PADDING, WIN.get_height() - TARGET_PADDING),
                )
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            if target.is_expired():
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if len(targets) > 0 and not targets[0].collide(*mouse_pos) and click:
            misses += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)
            run = False

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
