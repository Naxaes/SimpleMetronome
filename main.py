import pygame

SOUND_BUFFER_SIZE = 1024

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
FPS_CAP = 60

TITLE_FONT_SIZE = 16
TITLE_FONT_NAME = 'Courier New'  # Who doesn't prefer monospace fonts??

COLOR_BLACK = (0,   0,   0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0,   255, 0)

BACKGROUND_COLOR = COLOR_BLACK
TEXT_COLOR = COLOR_WHITE
DOT_COLOR  = COLOR_GREEN


# The buffer for the mixer is too large for my computer, which makes the latency to big.
# This initializes the buffer to 1024 instead of 4096 (they've changed this default quite a lot).
# The rest are the default values.
# https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.pre_init
pygame.mixer.pre_init(buffer=SOUND_BUFFER_SIZE)
pygame.init()

font   = pygame.font.SysFont(TITLE_FONT_NAME, TITLE_FONT_SIZE)
screen = pygame.display.set_mode(SCREEN_SIZE)

dot_timer = 0           # Keeps track on how long the dot has been displayed.
display_dot = False     # Whether to display the dot or not.

bpm = 120

clock = pygame.time.Clock()
sound = pygame.mixer.Sound('bop.wav')

time = 0
running = True

while running:
    dt = clock.tick(FPS_CAP)
    time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                bpm -= 5
            elif event.key == pygame.K_RIGHT:
                bpm += 5

    # Calculate how long to wait based on the bpm.
    beats_per_ms = (bpm / 60) / 1000
    ms_per_beat  = 1 / beats_per_ms  # How many milliseconds each beat takes.

    if time >= ms_per_beat:
        time -= ms_per_beat
        sound.play()
        display_dot = True
        dot_timer = ms_per_beat * 0.75

    screen.fill(BACKGROUND_COLOR)
    text_surface = font.render('BPM {}'.format(bpm), True, TEXT_COLOR)
    screen.blit(text_surface, (160, 20))

    if display_dot:
        dot_timer -= dt
        if dot_timer <= 0:
            display_dot = False
        pygame.draw.circle(screen, DOT_COLOR, (200, 200), 20)

    pygame.display.update()
