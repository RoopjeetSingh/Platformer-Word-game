import pygame as pg
import pygame.gfxdraw

pg.init()


def draw_rounded_rect(surface, rect, color, corner_radius):
    """ Draw a rectangle with rounded corners.
    Would prefer this:
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    but this option is not yet supported in my version of pygame so do it ourselves.

    We use anti-aliased circles to make the corners smoother
    """
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(
            f"Both height ({rect.height}) and width ({rect.width}) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius,
                            color)

    pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius,
                                 color)
    pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius,
                                 color)
    pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1,
                                 corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)


def draw_bordered_rounded_rect(surface, rect, color, border_color, corner_radius, border_thickness):
    if corner_radius < 0:
        raise ValueError(f"border radius ({corner_radius}) must be >= 0")

    rect_tmp = pygame.Rect(rect)

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect_tmp)
        else:
            draw_rounded_rect(surface, rect_tmp, border_color, corner_radius)

        rect_tmp.inflate_ip(-2 * border_thickness, -2 * border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect_tmp)
    else:
        draw_rounded_rect(surface, rect_tmp, color, inner_radius)


class Button:
    """A fairly straight forward button class."""

    def __init__(self, rect, color, function, text=None, font=pg.font.Font(None, 36), call_on_release=True,
                 hover_color=None, clicked_color=None, font_color=pg.Color("white"), hover_font_color=None,
                 clicked_font_color=None, click_sound=None, hover_sound=None, image=None, text_position=None,
                 image_position=None, border_radius=0, border_color=None, image_align=None, fill_bg=True,
                 border_thickness=7):

        self.image = image
        self.text = text
        self.font = font
        self.call_on_release = call_on_release
        self.hover_color = hover_color
        self.clicked_color = clicked_color
        self.font_color = font_color
        self.hover_font_color = hover_font_color
        self.clicked_font_color = clicked_font_color
        self.click_sound = click_sound
        self.hover_sound = hover_sound
        self.image_original = image
        self.text_position = text_position
        self.image_position = image_position
        self.border_radius = border_radius
        self.border_color = border_color
        self.image_align = image_align
        self.image_copy = self.image_original
        self.fill_bg = fill_bg
        self.border_thickness = border_thickness
        if self.image_original:
            self.image_copy = pygame.transform.scale(
                self.image_original, (self.image_original.get_width() - 15, self.image_original.get_height() - 15))

        self.rect_original = pg.Rect(rect)
        self.rect = self.rect_original.copy()
        self.rect_inflated = self.rect_original.inflate(-15, -15)
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
        self.image = self.image_original
        self.rect = self.rect_original

        self.check_hover()
        if self.clicked:
            if self.clicked_color:
                color = self.clicked_color
                if self.clicked_font_color:
                    text = self.clicked_text
            self.image = self.image_copy
            self.rect = self.rect_inflated
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.hover_font_color:
                text = self.hover_text

        if self.border_radius and self.border_color and not self.clicked:
            draw_bordered_rounded_rect(surface, self.rect, color, self.border_color, self.border_radius, self.border_thickness)
        elif self.border_radius:
            draw_rounded_rect(surface, self.rect, color, self.border_radius)
        elif self.fill_bg:
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
            text_rect.top = self.rect.y + (self.rect.height - self.image.get_height() - self.text.get_height() - 5) / 2
            surface.blit(self.image, image_rect)
            surface.blit(self.text, text_rect)
        elif self.image and self.image_align == "top" and self.text:
            image_rect = self.image.get_rect()
            image_rect.centerx = self.rect.centerx
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            image_rect.top = self.rect.y + (self.rect.height - self.image.get_height() - self.text.get_height()) / 2
            text_rect.bottom = self.rect.y + self.rect.height - \
                               (self.rect.height - self.image.get_height() - self.text.get_height()) / 2
            surface.blit(self.image, image_rect)
            surface.blit(self.text, text_rect)
        elif self.image and not self.image_position and not self.image_align:
            image_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, image_rect)
