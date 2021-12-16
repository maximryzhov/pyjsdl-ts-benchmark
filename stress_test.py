# Imports organized in order to work both with Pygame and Pyjsdl-ts
try:
    from pyjsdl.pylib import os
    import pyjsdl as pg
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
from sprite import RandomSprite

class Scene:
    def __init__(self, img, screen, num_spr_to_add, min_fps, end_callback):
        self.img = img
        self.screen = screen
        self.num_spr_to_add = num_spr_to_add
        self.min_fps = min_fps
        self.end_callback = end_callback

        self.sprites = []
        self.font = pg.font.SysFont(None, 24)
        self.fps_counter = FPSCounter()
        self.time_passed = 0
        self.started = False
        self.finished = False

    def run(self, events, dt):
        self.fps_counter.update(dt/1000)
        self.time_passed += dt

    def add_sprites(self, num):
        for _ in range(0, num):
            spr = RandomSprite(
                self.img, 0, 0, self.screen.get_width(), self.screen.get_height(), -100, 100
            )
            self.sprites.append(spr)

    def update_sprites(self, dt):
        for spr in self.sprites:
            spr.update(dt)

    def draw_sprites(self):
        for spr in self.sprites:
            spr.draw(self.screen)

    def draw_start_text(self):
        self.screen.blit(self.start_text, (self.screen.get_rect().centerx - self.start_text.get_rect(
        ).centerx, self.screen.get_rect().centery - self.start_text.get_rect().centery))

    def update_info(self):
        self.info_str = "Sprites: {} ".format(len(self.sprites))
        self.info_str += "FPS: {} ".format(int(self.fps_counter.get_fps()))
        self.info_str += "Time passed : {} ms".format(int(self.time_passed))

    def draw_info(self):
        info_text = self.font.render(self.info_str, True, (255, 255, 255))
        pg.draw.rect(self.screen, (0, 0, 0), info_text.get_rect())
        self.screen.blit(info_text, (4, 4))

    def draw_end_text(self):
        self.screen.blit(self.end_text, (self.screen.get_rect().centerx - self.end_text.get_rect(
        ).centerx, self.screen.get_rect().centery - self.end_text.get_rect().centery))

    def check_min_fps(self):
        if self.time_passed > 1000 and self.fps_counter.get_fps() < self.min_fps:
            self.finished = True

    def process_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                if not self.started:
                    self.started = True
                elif self.finished:
                    self.end_callback()
                    self.finished = False
                    self.time_passed = 0
                    self.sprites = []


class StaticTest(Scene):
    def __init__(self, img, screen, num_spr_to_add, min_fps, end_callback):
        Scene.__init__(self, img, screen, num_spr_to_add,
                       min_fps, end_callback)
        self.start_text = self.font.render(
            "Static objects test. Click to start", True, (0, 255, 0))
        self.end_text = self.font.render(
            "Minimal FPS reached. Click for dynamic objects test", True, (0, 255, 0))

    def run(self, events, dt):
        Scene.run(self, events, dt)
        self.process_events(events)

        if not self.started:
            self.draw_start_text()
        elif not self.finished:
            self.add_sprites(self.num_spr_to_add)
            self.draw_sprites()
            self.update_info()
            self.draw_info()
            self.check_min_fps()
        else:
            self.draw_info()
            self.draw_end_text()


class DynamicTest(Scene):
    def __init__(self, img, screen, num_spr_to_add, min_fps, end_callback):
        Scene.__init__(self, img, screen, num_spr_to_add,
                       min_fps, end_callback)
        self.started = True
        self.end_text = self.font.render(
            "Minimal FPS reached. Click for static objects test", True, (0, 255, 0))

    def run(self, events, dt):
        Scene.run(self, events, dt)
        self.process_events(events)

        if not self.finished:
            self.add_sprites(self.num_spr_to_add)
            self.update_sprites(dt/1000)
            self.draw_sprites()
            self.update_info()
            self.draw_info()
            self.check_min_fps()
        else:
            self.draw_info()
            self.draw_end_text()


class Game:
    #  __pragma__ ('kwargs')
    def __init__(self, screen_size, max_fps, num_spr_to_add, min_fps):
        self.screen_size = screen_size
        self.max_fps = max_fps
        self.num_spr_to_add = num_spr_to_add
        self.min_fps = min_fps

        self.img = None
        self.running = True

        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(screen_size)
        pg.display.set_caption("Snake stress test")

        if platform == "web":
            pg.setup(self.web_init, ["snake.png"])
        else:
            self.prerun()
            while self.running:
                self.game_loop()
    #  __pragma__ ('kwargs')

    def prerun(self):
        # Convert image for better performance
        self.img = pg.image.load(os.path.join(res_dir, "snake.png")).convert()
        # Scale it 2 times
        self.img = pg.transform.scale2x(self.img)

        # Setup 2 scenes with tests
        self.static_test = StaticTest(self.img, self.screen,
                                      self.num_spr_to_add, self.min_fps, lambda: self.switch_scene(self.dynamic_test))
        self.dynamic_test = DynamicTest(self.img, self.screen,
                                        self.num_spr_to_add, self.min_fps, lambda: self.switch_scene(self.static_test))
        self.scene = self.static_test

    def web_init(self):
        self.prerun()
        pg.set_callback(self.game_loop)

    def game_loop(self):
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                self.running = False

        self.screen.fill((0, 0, 0))

        dt = self.clock.get_time()
        self.scene.run(events, dt)

        pg.display.flip()

        self.clock.tick(self.max_fps)

    def switch_scene(self, scene):
        self.scene = scene


if __name__ == "__main__":
    screen_size = (800, 600)
    # Make standalone version to add x10 sprites more
    if platform == "web":
        num_spr_to_add = 1
    else:
        num_spr_to_add = 10
    game = Game(screen_size, max_fps=60, min_fps=30, num_spr_to_add=num_spr_to_add)
