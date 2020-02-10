import random
import sys
import pygame.locals
import params

from character import Character
from helpers.algorithm_runner import run_a_star

# Load images
gnd_imgs = [pygame.image.load('res/gnd1.png'), pygame.image.load('res/gnd2.png')]
block_img = pygame.image.load('res/block.png')
ch_img = pygame.image.load('res/tank.png')  # character

path = []  # the shortest path from character position to the goal point
cur_point_index = 0  # index of the current path point from which the character moves to the next one
dest_point = None  # current path point to which the character moves

# PyGame initialization
pygame.init()
screen = pygame.display.set_mode((params.WIDTH, params.HEIGHT))
pygame.display.set_caption('A* algorithm - 2D Tank')
pygame.display.set_icon(ch_img)
clock = pygame.time.Clock()

# Just to write less
ts = params.TILE_SIZE


def draw_map():
    """Draws map tiles."""
    for i, row in enumerate(MAP):
        for j, tile in enumerate(row):
            if tile == '_':
                screen.blit(gnd_imgs[0], (j * params.TILE_SIZE, i * params.TILE_SIZE))
            elif tile == '-':
                screen.blit(gnd_imgs[1], (j * params.TILE_SIZE, i * params.TILE_SIZE))
            elif tile == 'B':
                screen.blit(block_img, (j * params.TILE_SIZE, i * params.TILE_SIZE))


def draw_lines():
    """Draws lines between path points."""
    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]

        pygame.draw.line(screen, (255, 255, 255),
                         (a[1] * params.TILE_SIZE + params.TILE_SIZE // 2,
                          a[0] * params.TILE_SIZE + params.TILE_SIZE // 2),
                         (b[1] * params.TILE_SIZE + params.TILE_SIZE // 2,
                          b[0] * params.TILE_SIZE + params.TILE_SIZE // 2),
                         2)


def draw_goal():
    """Draws goal point."""
    # Make goal point transparent
    end_rect = pygame.Surface((ts, ts))
    end_rect.set_alpha(64)
    end_rect.fill((255, 255, 255))
    screen.blit(end_rect, (goal[1] * ts, goal[0] * ts))


def move_character():
    """Moves character along the path."""
    global cur_point_index, dest_point

    # Make the character continue movement from its current position and not go back to the first tile if its current
    #   destination and the second point are the same. That kind of situation happens when a new path is found.
    if cur_point_index + 1 < len(path):
        if path[cur_point_index + 1] == dest_point:
            cur_point_index += 1

    # Move character from the current point to the next point
    if cur_point_index < len(path):
        dest_point = (path[cur_point_index][0], path[cur_point_index][1])
        to_x = path[cur_point_index][1] * params.TILE_SIZE
        to_y = path[cur_point_index][0] * params.TILE_SIZE
        ch.move(to_x, to_y)

        # Change the current point
        if ch.x == to_x and ch.y == to_y:
            cur_point_index += 1


def handle_input():
    """Handles inputs (events)."""
    global goal, path, cur_point_index
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            return True
    # Create or delete a block
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        col = pos[0] // ts
        row = pos[1] // ts
        keys = pygame.key.get_pressed()

        # Delete the block if the left mouse button is clicked and ctrl key is pressed
        if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and MAP[row][col] == 'B':
            MAP[row][col] = random.choice(('_', '-'))
        # Create a block if the left mouse button is clicked and ctrl key is not pressed
        elif not keys[pygame.K_LCTRL]:
            # Make sure the block doesn't collide with the character
            ch_rect = pygame.Rect(int(ch.x), int(ch.y), ts, ts)
            if not ch_rect.colliderect((col * ts, row * ts, ts, ts)):
                MAP[row][col] = 'B'

        # Find the shortest path in changed world
        if goal is not None:
            path = find_path()
            cur_point_index = 0

    # Set the goal point if the right mouse button is clicked
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        col = pos[0] // ts
        row = pos[1] // ts
        if MAP[row][col] != 'B':
            goal = row, col

            # Find the shortest path to the new goal point
            path = find_path()
            cur_point_index = 0

    return False


def find_path():
    """Finds the shortest path from character position to the goal."""
    # Find the tile on which the character is "standing"
    start_row = int(ch.y // params.TILE_SIZE)
    start_col = int(ch.x // params.TILE_SIZE)

    return run_a_star(MAP, (start_row, start_col), goal)


def start():
    """Starts the game. Contains main loop."""
    global goal, path, cur_point_index

    # Main loop
    while True:
        """Input"""
        if handle_input():
            return

        """Update"""
        move_character()

        """Drawing"""
        draw_map()
        draw_lines()
        ch.draw(screen)
        if goal is not None:
            draw_goal()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    while True:
        # Create an empty map
        MAP = [
            [random.choice(('-', '_')) for _ in range(params.COL_COUNT)] for _ in range(params.ROW_COUNT)
        ]

        # Create the main character
        ch = Character(0, 0, ch_img, params.CH_SPEED)

        # End point
        goal = None

        # Start the game
        start()
