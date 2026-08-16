# Chrome Dino Runner
# Pygame + Pygbag Web Compatible Version

import os
import random
import datetime
import asyncio

import pygame


# =========================================================
# INITIALIZATION
# =========================================================

pygame.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dino Runner")


# =========================================================
# ASSETS
# =========================================================

Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)


RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]

JUMPING = pygame.image.load(
    os.path.join("assets/Dino", "DinoJump.png")
)

DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]


SMALL_CACTUS = [
    pygame.image.load(
        os.path.join("assets/Cactus", "SmallCactus1.png")
    ),
    pygame.image.load(
        os.path.join("assets/Cactus", "SmallCactus2.png")
    ),
    pygame.image.load(
        os.path.join("assets/Cactus", "SmallCactus3.png")
    ),
]


LARGE_CACTUS = [
    pygame.image.load(
        os.path.join("assets/Cactus", "LargeCactus1.png")
    ),
    pygame.image.load(
        os.path.join("assets/Cactus", "LargeCactus2.png")
    ),
    pygame.image.load(
        os.path.join("assets/Cactus", "LargeCactus3.png")
    ),
]


BIRD = [
    pygame.image.load(
        os.path.join("assets/Bird", "Bird1.png")
    ),
    pygame.image.load(
        os.path.join("assets/Bird", "Bird2.png")
    ),
]


CLOUD = pygame.image.load(
    os.path.join("assets/Other", "Cloud.png")
)

BG = pygame.image.load(
    os.path.join("assets/Other", "Track.png")
)


# =========================================================
# GLOBAL VARIABLES
# =========================================================

FONT_COLOR = (0, 0, 0)

game_speed = 20
x_pos_bg = 0
y_pos_bg = 380

points = 0
high_score = 0


# =========================================================
# DINOSAUR CLASS
# =========================================================

class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340

    JUMP_VEL = 8.5

    def __init__(self):

        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0

        self.jump_vel = self.JUMP_VEL

        self.image = self.run_img[0]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):

        if self.dino_duck:
            self.duck()

        if self.dino_run:
            self.run()

        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        # Jump
        if (
            userInput[pygame.K_UP]
            or userInput[pygame.K_SPACE]
        ) and not self.dino_jump:

            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True

        # Duck
        elif (
            userInput[pygame.K_DOWN]
            and not self.dino_jump
        ):

            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False

        # Run
        elif not (
            self.dino_jump
            or userInput[pygame.K_DOWN]
        ):

            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):

        self.image = self.duck_img[
            self.step_index // 5
        ]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK

        self.step_index += 1

    def run(self):

        self.image = self.run_img[
            self.step_index // 5
        ]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.step_index += 1

    def jump(self):

        self.image = self.jump_img

        self.dino_rect.y -= self.jump_vel * 4

        self.jump_vel -= 0.8

        if self.jump_vel < -self.JUMP_VEL:

            self.dino_jump = False

            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):

        screen.blit(
            self.image,
            (
                self.dino_rect.x,
                self.dino_rect.y
            )
        )


# =========================================================
# CLOUD CLASS
# =========================================================

class Cloud:

    def __init__(self):

        self.x = SCREEN_WIDTH + random.randint(
            800,
            1000
        )

        self.y = random.randint(
            50,
            100
        )

        self.image = CLOUD

        self.width = self.image.get_width()

    def update(self):

        self.x -= game_speed

        if self.x < -self.width:

            self.x = (
                SCREEN_WIDTH
                + random.randint(2500, 3000)
            )

            self.y = random.randint(
                50,
                100
            )

    def draw(self, screen):

        screen.blit(
            self.image,
            (
                self.x,
                self.y
            )
        )


# =========================================================
# OBSTACLE CLASS
# =========================================================

class Obstacle:

    def __init__(self, image, type):

        self.image = image

        self.type = type

        self.rect = self.image[
            self.type
        ].get_rect()

        self.rect.x = SCREEN_WIDTH

    def update(self):

        self.rect.x -= game_speed

        if self.rect.x < -self.rect.width:

            if self in obstacles:
                obstacles.remove(self)

    def draw(self, screen):

        screen.blit(
            self.image[self.type],
            self.rect
        )


# =========================================================
# SMALL CACTUS
# =========================================================

class SmallCactus(Obstacle):

    def __init__(self, image):

        self.type = random.randint(0, 2)

        super().__init__(
            image,
            self.type
        )

        self.rect.y = 325


# =========================================================
# LARGE CACTUS
# =========================================================

class LargeCactus(Obstacle):

    def __init__(self, image):

        self.type = random.randint(0, 2)

        super().__init__(
            image,
            self.type
        )

        self.rect.y = 300


# =========================================================
# BIRD
# =========================================================

class Bird(Obstacle):

    BIRD_HEIGHTS = [
        250,
        290,
        320
    ]

    def __init__(self, image):

        self.type = 0

        super().__init__(
            image,
            self.type
        )

        self.rect.y = random.choice(
            self.BIRD_HEIGHTS
        )

        self.index = 0

    def draw(self, screen):

        if self.index >= 10:
            self.index = 0

        screen.blit(
            self.image[self.index // 5],
            self.rect
        )

        self.index += 1


# =========================================================
# BACKGROUND
# =========================================================

def background():

    global x_pos_bg
    global y_pos_bg

    image_width = BG.get_width()

    SCREEN.blit(
        BG,
        (
            x_pos_bg,
            y_pos_bg
        )
    )

    SCREEN.blit(
        BG,
        (
            image_width + x_pos_bg,
            y_pos_bg
        )
    )

    if x_pos_bg <= -image_width:

        x_pos_bg = 0

    x_pos_bg -= game_speed


# =========================================================
# SCORE
# =========================================================

def draw_score(font):

    global points
    global high_score

    text = font.render(
        "High Score: "
        + str(high_score)
        + "  Points: "
        + str(points),
        True,
        FONT_COLOR
    )

    text_rect = text.get_rect()

    text_rect.center = (
        900,
        40
    )

    SCREEN.blit(
        text,
        text_rect
    )


# =========================================================
# GAME
# =========================================================

async def main():

    global game_speed
    global x_pos_bg
    global y_pos_bg
    global points
    global obstacles
    global high_score
    global FONT_COLOR

    clock = pygame.time.Clock()

    player = Dinosaur()

    cloud = Cloud()

    game_speed = 20

    x_pos_bg = 0

    y_pos_bg = 380

    points = 0

    obstacles = []

    font = pygame.font.Font(
        None,
        20
    )

    running = True

    while running:

        # =============================================
        # EVENTS
        # =============================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return False

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):

                return False

        # =============================================
        # DAY / NIGHT
        # =============================================

        current_time = datetime.datetime.now().hour

        if 7 < current_time < 19:

            FONT_COLOR = (
                0,
                0,
                0
            )

            SCREEN.fill(
                (
                    255,
                    255,
                    255
                )
            )

        else:

            FONT_COLOR = (
                255,
                255,
                255
            )

            SCREEN.fill(
                (
                    128,
                    128,
                    128
                )
            )

        # =============================================
        # USER INPUT
        # =============================================

        userInput = pygame.key.get_pressed()

        # =============================================
        # PLAYER
        # =============================================

        player.update(
            userInput
        )

        player.draw(
            SCREEN
        )

        # =============================================
        # OBSTACLES
        # =============================================

        if len(obstacles) == 0:

            choice = random.randint(
                0,
                2
            )

            if choice == 0:

                obstacles.append(
                    SmallCactus(
                        SMALL_CACTUS
                    )
                )

            elif choice == 1:

                obstacles.append(
                    LargeCactus(
                        LARGE_CACTUS
                    )
                )

            else:

                obstacles.append(
                    Bird(
                        BIRD
                    )
                )

        for obstacle in obstacles:

            obstacle.draw(
                SCREEN
            )

            obstacle.update()

            # Collision
            if player.dino_rect.colliderect(
                obstacle.rect
            ):

                if points > high_score:

                    high_score = points

                pygame.display.update()

                await asyncio.sleep(
                    1
                )

                return True

        # =============================================
        # BACKGROUND
        # =============================================

        background()

        # =============================================
        # CLOUD
        # =============================================

        cloud.draw(
            SCREEN
        )

        cloud.update()

        # =============================================
        # SCORE
        # =============================================

        points += 1

        if points % 100 == 0:

            game_speed += 1

        if points > high_score:

            high_score = points

        draw_score(
            font
        )

        # =============================================
        # DISPLAY
        # =============================================

        pygame.display.update()

        clock.tick(30)

        # VERY IMPORTANT FOR PYGBAG
        await asyncio.sleep(0)


# =========================================================
# MENU
# =========================================================

async def menu(death_count):

    global FONT_COLOR

    font = pygame.font.Font(
        None,
        30
    )

    while True:

        # =============================================
        # DAY / NIGHT
        # =============================================

        current_time = datetime.datetime.now().hour

        if 7 < current_time < 19:

            FONT_COLOR = (
                0,
                0,
                0
            )

            SCREEN.fill(
                (
                    255,
                    255,
                    255
                )
            )

        else:

            FONT_COLOR = (
                255,
                255,
                255
            )

            SCREEN.fill(
                (
                    128,
                    128,
                    128
                )
            )

        # =============================================
        # MENU TEXT
        # =============================================

        if death_count == 0:

            text = font.render(
                "Press any Key to Start",
                True,
                FONT_COLOR
            )

        else:

            text = font.render(
                "Press any Key to Restart",
                True,
                FONT_COLOR
            )

            score_text = font.render(
                "Your Score: "
                + str(points),
                True,
                FONT_COLOR
            )

            score_rect = score_text.get_rect()

            score_rect.center = (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 50
            )

            SCREEN.blit(
                score_text,
                score_rect
            )

            high_score_text = font.render(
                "High Score: "
                + str(high_score),
                True,
                FONT_COLOR
            )

            high_score_rect = (
                high_score_text.get_rect()
            )

            high_score_rect.center = (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 100
            )

            SCREEN.blit(
                high_score_text,
                high_score_rect
            )

        # =============================================
        # MAIN MENU TEXT
        # =============================================

        text_rect = text.get_rect()

        text_rect.center = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

        SCREEN.blit(
            text,
            text_rect
        )

        # Dino image

        SCREEN.blit(
            RUNNING[0],
            (
                SCREEN_WIDTH // 2 - 20,
                SCREEN_HEIGHT // 2 - 140
            )
        )

        pygame.display.update()

        # =============================================
        # EVENTS
        # =============================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return False

            if event.type == pygame.KEYDOWN:

                return True

        # VERY IMPORTANT FOR PYGBAG

        await asyncio.sleep(0)


# =========================================================
# GAME CONTROLLER
# =========================================================

async def game():

    death_count = 0

    while True:

        # Show menu

        start_game = await menu(
            death_count
        )

        # User closed game

        if not start_game:

            break

        # Start game

        died = await main()

        # User closed game

        if died is False:

            break

        # Player died

        death_count += 1

    pygame.quit()


# =========================================================
# START GAME
# =========================================================

if __name__ == "__main__":

    asyncio.run(
        game()
    )