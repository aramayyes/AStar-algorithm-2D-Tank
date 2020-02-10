import math
import pygame


class Character:
    """Represents a single character."""

    def __init__(self, x, y, img, speed=1):
        self.x = x
        self.y = y
        self.orig_img = img
        self.img = img
        self.speed = speed * 0.5

        self.angle = 0

    def move(self, to_x, to_y):
        """Moves the current character towards the given position."""
        if self.x == to_x and self.y == to_y:
            return

        # Find out the direction
        dir_x = to_x - self.x
        dir_y = to_y - self.y
        if dir_x != 0:
            dir_x = 1 if dir_x > 0 else -1
        if dir_y != 0:
            dir_y = 1 if dir_y > 0 else -1

        # Move the character and make sure it doesn't move more than necessary
        if (dir_x > 0 and self.x + self.speed > to_x) or (dir_x < 0 and self.x - self.speed < to_x):
            self.x = to_x
        else:
            self.x += self.speed * dir_x
        if (dir_y > 0 and self.y + self.speed > to_y) or (dir_y < 0 and self.y - self.speed < to_y):
            self.y = to_y
        else:
            self.y += self.speed * dir_y

        # Rotate the character to look in the new direction
        self.rotate((dir_x, dir_y))

    def rotate(self, direction):
        """Rotates the current character if needed so that it looks in the given direction."""
        # Calculate the angle
        dir_x, dir_y = direction
        length = math.sqrt(math.fabs(dir_x) + math.fabs(dir_y))
        angle = math.degrees(math.acos(dir_x / length))
        if dir_y != 0:
            angle *= -dir_y

        # Don't rotate the image if it already looks in the desired direction
        if self.angle == angle:
            return

        self.img = pygame.transform.rotate(self.orig_img, angle)
        self.angle = angle

    def draw(self, screen):
        """Draws the character to the screen."""
        screen.blit(self.img, (self.x, self.y))
