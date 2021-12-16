# Imports organized in order to work both with Pygame and Pyjsdl-ts
try:
    from pyjsdl.pylib import os
    import pyjsdl as pg
    from pyjsdl.vector import Vector2
    platform = "web"
    res_dir = ""
except NameError:
    pass

# __pragma__('skip')
import os
import pygame as pg
platform = "standalone"
res_dir = "public"
# __pragma__('noskip')

from fps_counter import FPSCounter
from widgets import Button, Label, HBox, VBox, Widget
from sprite import RandomSprite


class Game:
    def __init__(self, screen_size, max_fps):
        self.screen_size = screen_size
        self.max_fps = max_fps

        self.img = None
        self.sprites = []
        self.sprites_moving = True

        self.fps_counter = FPSCounter()
        self.running = True
        
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(screen_size)
        pg.display.set_caption("Snake mark")

        # Create some UI
        self.ui_root = Widget(None, 0, 0, self.screen_size[0], self.screen_size[1])
        
        hbox = HBox(self.ui_root, h_anchor="right")
        Button(hbox, "+ 100", lambda: self.add_sprites(100))
        Button(hbox, "- 100", lambda: self.remove_sprites(100))
        self.toggle_btn = Button(hbox, "Stop", self.toggle_moving)
        Button(hbox, "Clear", self.clear)
        hbox.layout()
        
        vbox = VBox(self.ui_root, spacing=0, h_anchor="left")
        self.fps_label = Label(vbox, "FPS:", w=120)
        self.sprite_count_label = Label(vbox, "Sprites:", w=120)
        vbox.layout()
              
        if platform == "web":
            pg.setup(self.web_init,["snake.png"])
        else:
            self.prerun()
            while self.running:
                self.game_loop()

    def add_sprites(self, num):
        for _ in range(0, num):
            spr = RandomSprite(self.img, 0, 0, self.screen_size[0], self.screen_size[1], -100, 100)
            self.sprites.append(spr)

    def remove_sprites(self, num):
        if len(self.sprites) >= num:
            self.sprites = self.sprites[num:]

    def toggle_moving(self):
        if self.sprites_moving:
            self.sprites_moving = False
            self.toggle_btn.set_text("Move")
        else:
            self.sprites_moving = True
            self.toggle_btn.set_text("Stop")

    def clear(self):
        self.sprites = []

    def prerun(self):
        # Convert image for better performance
        self.img = pg.image.load(os.path.join(res_dir, "snake.png")).convert()
        # Scale it 2 times
        self.img = pg.transform.scale2x(self.img)
        self.add_sprites(100)

    def web_init(self):
        self.prerun()
        pg.set_callback(self.game_loop)

    def game_loop(self):
        for e in pg.event.get():
            if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                self.running = False

        self.screen.fill((0, 0, 0))

        dt = self.clock.get_time() / 1000

        for spr in self.sprites:
            if self.sprites_moving:
                spr.update(dt)
            spr.draw(self.screen)

        for e in self.ui_root.children:
            e.update(dt)
            e.draw(self.screen)

        self.fps_counter.update(dt)
        # Pyjsdl doesn't support Python 3 string interpolation
        self.sprite_count_label.set_text("Sprites: {}".format(len(self.sprites)))
        self.fps_label.set_text("FPS: {}".format(self.fps_counter.get_fps()))

        pg.display.flip()

        self.clock.tick(self.max_fps)


if __name__ == "__main__":
    # Transcrypt needs compiler directives to use __getitem__ method for Vector
    screen_size = (800, 600)
    max_fps = 60
    game = Game(screen_size, max_fps)
