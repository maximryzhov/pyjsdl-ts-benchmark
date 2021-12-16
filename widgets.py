# Simple UI classes for pygame demo
# TODO: auto layout, propagate events

# Imports organized in order to work both with Pygame and Pyjsdl-ts
try:
    import pyjsdl as pg
    from pyjsdl.surface import Surface
except NameError:
    pass

# __pragma__('skip')
import pygame as pg
from pygame.surface import Surface
# __pragma__('noskip')

class Widget:
    #  __pragma__ ('kwargs')
    def __init__(self, parent, x, y, w, h, padding=0):
        self.rect = pg.Rect(x, y, w, h)
        self.padding = padding
        self.children = []
        self.parent = parent
        if self.parent:
            self.parent.add(self)
        self.debug = False

    def add(self, child):
        self.children.append(child)

    def redraw(self):
        for w in self.children:
            w.redraw()

    def layout(self):
        pass

    def update(self, dt):
        for w in self.children:
            w.update(dt)

    def draw(self, surf):
        for w in self.children:
            w.draw(surf)
        if self.debug:
            pg.draw.rect(surf, (255, 0, 0), self.rect, 1)


class TextWidget(Widget):
    """
    Widget containing text with 'display: block' and 'align: center' behaviour
    """
    FONT_COLOR = (0, 0, 0)
    #  __pragma__ ('kwargs')
    def __init__(self, parent, text, x=0, y=0, w=100, h=30, padding=4, font_size=16):
        # Transcrypt doesn't support super() with arguments
        super().__init__(parent, x, y, w, h, padding)
        self.text = text
        self.font_size = font_size
        self.redraw()
    #  __pragma__ ('nokwargs')

    def make_text_clip_rect(self, text_rect):
        # Try to center text horizontally
        if text_rect.w < self.rect.w:
            h_padding = (self.rect.w - text_rect.w) / 2
        else:
            h_padding = self.padding
        # Try to center text vertically
        if text_rect.h < self.rect.h:
            v_padding = (self.rect.h - text_rect.h) / 2
        else:
            v_padding = self.padding
        return pg.Rect(
            -h_padding,
            -v_padding,
            self.rect.w - h_padding,
            self.rect.h - v_padding,
        )

    def make_bg(self, color, text_surface, text_clipping_rect):
        surface = Surface(self.rect.size)
        surface.fill(color)
        surface.blit(text_surface, (0, 0), text_clipping_rect)
        return surface.convert()

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self.redraw()


class Label(TextWidget):
    """
    Simple text label
    """

    BG_COLOR = (64, 64, 64)
    FONT_COLOR = (255, 255, 255)

    def redraw(self):
        font = pg.font.SysFont(None, self.font_size)
        text_surface = font.render(self.text, True, self.FONT_COLOR)
        text_clip_rect = self.make_text_clip_rect(text_surface.get_rect())
        self.surface = self.make_bg(
            self.BG_COLOR, text_surface, text_clip_rect)
        # Transcrypt doesn't support super() with arguments
        super().redraw()

    def draw(self, surf):
        surf.blit(self.surface, self.rect)
        # Transcrypt doesn't support super() with arguments
        super().draw(surf)


class Button(TextWidget):
    """
    3-state button with text and onclick callback
    """

    STATE_IDLE = 0
    STATE_HOVER = 1
    STATE_PRESSED = 2

    BG_IDLE = (191, 191, 191)
    BG_HOVER = (240, 240, 240)
    BG_PRESSED = (160, 160, 160)

    #  __pragma__ ('kwargs')
    def __init__(self, parent, text, onclick, x=0, y=0, w=100, h=30, padding=4, font_size=16):
        # Transcrypt doesn't support super() with arguments
        super().__init__(
            parent, text, x, y, w, h, padding, font_size)
        self.onclick = onclick
        self.state = self.STATE_IDLE
        self.redraw()
    #  __pragma__ ('nokwargs')        

    def redraw(self):
        font = pg.font.SysFont(None, self.font_size)
        text_surface = font.render(self.text, True, self.FONT_COLOR)
        text_clip_rect = self.make_text_clip_rect(text_surface.get_rect())
        self.bg_idle_surface = self.make_bg(
            self.BG_IDLE, text_surface, text_clip_rect)
        self.bg_hover_surface = self.make_bg(
            self.BG_HOVER, text_surface, text_clip_rect
        )
        self.bg_pressed_surface = self.make_bg(
            self.BG_PRESSED, text_surface, text_clip_rect
        )
        # Transcrypt doesn't support super() with arguments
        super().redraw()

    def update(self, dt):
        hover = self.rect.collidepoint(pg.mouse.get_pos())
        left_click = pg.mouse.get_pressed()[0]

        if hover:
            if left_click:
                if self.state != self.STATE_PRESSED:
                    self.state = self.STATE_PRESSED
                    self.onclick()
            else:
                self.state = self.STATE_HOVER
        else:
            self.state = self.STATE_IDLE
        # Transcrypt doesn't support super() with arguments
        # Transcript doesn't support super() call of indirectly inherited methods
        TextWidget.update(self, dt)

    def draw(self, surf):
        if self.state == self.STATE_IDLE:
            surface = self.bg_idle_surface
        elif self.state == self.STATE_HOVER:
            surface = self.bg_hover_surface
            surf.blit(self.bg_hover_surface, self.rect)
        else:
            surface = self.bg_pressed_surface
        surf.blit(surface, self.rect)
        # Transcrypt doesn't support super() with arguments
        super().draw(surf)


class Box(Widget):
    """
    Abstract class for box sizers
    """
    #  __pragma__ ('kwargs')
    def __init__(self, parent, padding=4, spacing=5, h_anchor="left"):
		# Transcrypt doesn't support super() with arguments
        super().__init__(parent, parent.rect.x, parent.rect.y,
                         parent.rect.width, parent.rect.height, padding=padding,)
        self.spacing = spacing
        self.h_anchor = h_anchor
    #  __pragma__ ('nokwargs')    


class HBox(Box):
    """
    Stacks items horizontally in parent container
    """

    def layout(self):
        if not self.children:
            return
        max_height = 0

        self.rect.width = self.rect.left + self.padding

        for i, w in enumerate(self.children):
            w.rect.y = self.padding
            if w.rect.height > max_height:
                max_height = w.rect.height
            spacing = 0 if i == 0 else self.spacing
            w.rect.x = self.rect.width + spacing
            self.rect.width += w.rect.width + spacing

        self.rect.width += self.padding
        self.rect.height = self.padding + max_height + self.padding

        if self.h_anchor == "right":
            new_x = self.parent.rect.width - self.rect.width
            diff = new_x - self.rect.x
            for w in list(self.children):
                w.rect.x += diff
            self.rect.x = new_x
		# Transcrypt doesn't support super() with arguments
        super().layout()


class VBox(Box):
    """
    Stacks items vertically in parent container
    """

    def layout(self):
        if not self.children:
            return
        self.rect.width = max(
            [w.rect.width for w in self.children]) + self.padding * 2
        if self.h_anchor == "right":
            self.rect.x = self.parent.rect.width - self.rect.width
        self.rect.height = self.padding

        for i, w in enumerate(self.children):
            w.rect.x = self.rect.x + self.padding
            spacing = 0 if i == 0 else self.spacing
            w.rect.y = self.rect.y + self.rect.height + spacing
            self.rect.height += w.rect.h + self.spacing
        self.rect.height += self.padding
		# Transcrypt doesn't support super() with arguments
        super().layout()