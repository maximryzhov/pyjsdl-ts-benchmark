# Imports organized in order to work both with Pygame and Pyjsdl-ts
import random

try:
    from pyjsdl.vector import Vector2
except NameError:
    pass

# __pragma__('skip')
from pygame.math import Vector2
# __pragma__('noskip')

class RandomSprite:
    """
    Sprite appears at random coordinates
    and moves with random speed in random direction
    """

    def __init__(self, image, min_x, min_y, max_x, max_y, min_speed, max_speed):
        self.image = image

        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        self.position = Vector2(x, y)

        vx = random.randint(min_speed, max_speed)
        vy = random.randint(min_speed, max_speed)
        self.velocity = Vector2(vx, vy)

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def update(self, dt):
        # Bounce around
        if self.position.x < self.min_x and self.velocity.x < 0:
            self.position.x = self.min_x
            self.velocity.x = -self.velocity.x
        if self.position.x > self.max_x and self.velocity.x > 0:
            self.position.x = self.max_x
            self.velocity.x = -self.velocity.x
        if self.position.y < self.min_y and self.velocity.y < 0:
            self.position.y = self.min_y
            self.velocity.y = -self.velocity.y
        if self.position.y > self.max_y and self.velocity.y > 0:
            self.position.y = self.max_y
            self.velocity.y = -self.velocity.y

        # Move to a new position
        # __pragma__('opov')
        self.position += self.velocity * dt
        # __pragma__('noopov')

    def draw(self, surf):
        rect = self.image.get_rect()
        rect.x += self.position.x
        rect.y += self.position.y
        surf.blit(self.image, rect)