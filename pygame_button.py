#!/usr/bin/env python3


import pygame as pg
from rounded_rect import draw_rounded_rect, draw_bordered_rounded_rect


class Button:
    """A fairly straight forward button class."""

    def __init__(self, rect, color, function, **kwargs):
        self.process_kwargs(kwargs)
        self.rect = pg.Rect(rect)
        self.color = color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.render_text()

    def process_kwargs(self, kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {
            "text": None,
            "font": pg.font.Font(None, 36),
            "call_on_release": True,
            "hover_color": None,
            "clicked_color": None,
            "font_color": pg.Color("white"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
            "image": None,
            "text_position": (),
            "image_position": (),
            "image_align": None,
            "border_radius": 0,
            "border_color": None
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        """Pre render the button text."""
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text, True, color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text, True, color)
            self.text = self.font.render(self.text, True, self.font_color)

    def check_event(self, event):
        """The button needs to be passed events from your program event loop."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            self.function()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def update(self, surface):
        """Update needs to be called every frame in the main loop."""
        color = self.color
        text = self.text
        self.check_hover()
        if self.clicked and self.clicked_color:
            color = self.clicked_color
            if self.clicked_font_color:
                text = self.clicked_text
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.hover_font_color:
                text = self.hover_text
        if self.border_radius and self.border_color:
            draw_bordered_rounded_rect(surface, self.rect.inflate(-4, -4), color, self.border_color, self.border_radius, 7)
        elif self.border_radius:
            draw_rounded_rect(surface, self.rect.inflate(-4, -4), color, self.border_radius)
        else:
            surface.fill(pg.Color("black"), self.rect)
            surface.fill(color, self.rect.inflate(-4, -4))
        if self.text and not self.text_position and not self.image:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        elif self.text and self.text_position:
            surface.blit(text, (self.rect.x + self.text_position[0], self.rect.y + self.text_position[1]))
        if self.image and self.image_position:
            surface.blit(self.image, (self.rect.x + self.image_position[0], self.rect.y + self.image_position[1]))
        elif self.image and self.image_align == "bottom":
            image_rect = self.image.get_rect()
            image_rect.centerx = self.rect.centerx
            image_rect.bottom = self.rect.y + self.rect.height - \
                                (self.rect.height - self.image.get_height() - self.text.get_height() - 5) / 2
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.top = self.rect.y + (self.rect.height - self.image.get_height() - self.text.get_height() - 5)/2
            surface.blit(self.image, image_rect)
            surface.blit(self.text, text_rect)
        elif self.image and self.image_align == "top" and self.text:
            image_rect = self.image.get_rect()
            image_rect.centerx = self.rect.centerx
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            image_rect.top = self.rect.y + (self.rect.height - self.image.get_height() - self.text.get_height())/2
            text_rect.bottom = self.rect.y + self.rect.height - \
                                (self.rect.height - self.image.get_height() - self.text.get_height())/2
            surface.blit(self.image, image_rect)
            surface.blit(self.text, text_rect)
        elif self.image and not self.image_position and not self.image_align:
            image_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, image_rect)
